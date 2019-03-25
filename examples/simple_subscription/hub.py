# configure this as the hub of the group
import os

os.environ['NET_IS_HUB'] = 'True'

# Importing the application code will automatically launch the peer and begin
# listening for connection requests as well as set up the connection registry.
import app

if __name__ == '__main__':
    print("Enter the message to send to the peers subscribed to you.")
    while 1:
        # As you can imagine, this can be used anywhere in your application. In
        # this example, we are just going to take your message and broadcast it
        # to all the subscribed peers.
        your_message = input("Message: ")

        # This will trigger the "myEvent" that was wrapped on around this
        # function. When this is triggered, it will package up your message and
        # send it to the peers.
        app.something_happened(your_message)
