# imports
import os

# configure our net configuration with a group identifier
os.environ['NET_GROUP'] = 'app_v2'

# net imports
import net


# application code version 2
@net.connect("myTaggedFunction")
def connected_function(message):
    """
    This will return the message with the " Version 2" appended to the end.
    """
    return message + ' Version 2'
