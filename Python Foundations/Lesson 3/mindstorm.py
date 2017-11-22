import turtle
def draw_circle(drawer,radius):
    drawer.circle(radius)
def draw_square(drawer):
    for _ in range(4):
        drawer.forward(100)
        drawer.right(90)
    
def draw_shapes():
    window = turtle.Screen()
    window.bgcolor('blue')
    
    # drawing square
    zekas = turtle.Turtle()
    zekas.shape('turtle')
    zekas.color('#7FB414')
    zekas.speed(0)
    for _ in range(180):
        draw_square(zekas)
        zekas.right(2)
    
    """
    # drawing circle
    swaaf = turtle.Turtle()
    swaaf.shape('circle')
    swaaf.color('red')
    swaaf.speed(3)
    draw_circle(swaaf, 100)
    """
    # drawing triangle
    omar = turtle.Turtle()
    omar.shape('triangle')
    omar.color('black')
    omar.speed(0)
    for _ in range(180):
        draw_triangle(omar)
        omar.right(2)
    

    window.exitonclick()

def draw_triangle(drawer):
    
    drawer.forward(100)
    drawer.left(120)
    drawer.forward(100)
    drawer.left(120)
    drawer.forward(142)
    
    
draw_shapes()
