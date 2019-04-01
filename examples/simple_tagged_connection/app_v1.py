# imports
import os

# configure our net configuration with a group identifier
os.environ['NET_GROUP'] = 'app_v1'

# net imports
import net


# application code version 1
@net.connect("myTaggedFunction")  # <- this can be any value.
def connected_function(message):
    """
    This will return the message with the " Version 1" appended to the end.
    """
    return message + ' Version 1'
