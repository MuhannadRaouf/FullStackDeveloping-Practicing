# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioResetClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC49e03a984dbeb82a9e97c923ccd2b554"
auth_token = "16c7e891fcd07f2d47a8b915956abe9c"
client = TwilioResetClient(account_sid, auth_token)

message = client.sms.messages.create(
    body = "Do you love Muhannad ? \nIf YES tell him\nIf NO -_- THROW YOURSELF FROM THE CAR.",
    to = "+201118898519",
    from_ = "+15028068668")

print(message.sid)
