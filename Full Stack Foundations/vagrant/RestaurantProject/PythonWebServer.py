from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                for item in restaurants:
                    output += item.name
                    # objective 2 -- Add Edit and Delete links
                    output += "<br>" \
                              "<a href = 'restaurants/%s/edit'>Edit</a><br>" % item.id
                    output += "<br>" \
                              "<a href = 'restaurants/%s/delete'>Delete</a><br>" % item.id
                    output += "<br><br><br>"
                # objective 3 step 1 -- Adding link to add new restaurant
                output += "<a href = '/restaurants/new'>Add a new Restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            # Objective 3 step 2 -- adding a page for the new restaurant
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>" \
                          "<h1>What is the name of the new restaurant?</h1>" \
                          "<br><br>" \
                          "<input name = 'newRestaurant' type = 'text'>" \
                          "<input type = 'submit' value = 'Create'>" \
                          "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            # Objective 5 step 2 -- adding a page for confirm the deletion
            if self.path.endswith('/delete'):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete?</h1>"
                    output += "<form method ='POST' enctype ='multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Yes'>" \
                              "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return

            # Objective 4 step 1 -- adding a page for editing the name of the restaurant
            if self.path.endswith('/edit'):

                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % myRestaurantQuery.name
                    output += "<form method ='POST' enctype ='multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder= '%s'>" \
                              "<input type = 'submit' value = 'Edit' >" \
                              "</form>" % myRestaurantQuery.name
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
        except IOError:
            print("404 file not found %s " % self.path)

        return

    # Objective 3 step 3 -- Adding POST Methods
    def do_POST(self):
        try:
            if self.path.endswith('/delete'):
                # get the header content
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # Checking if there's data entered in the form in the get Method
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantIdPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).one()
                    if myRestaurantQuery:                        
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_header()
                return
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIdPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).one()
                    if myRestaurantQuery:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_header()
                return

            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurant')
                    # Creating new restaurant object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass


"""" Main"""


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web server is running on port 8080")
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C is captured, Stopping Web server...")
        server.socket.close()


if __name__ == "__main__":
    main()
