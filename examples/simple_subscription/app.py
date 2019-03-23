# configure this application as having its own network group through the
# environment set up
import os

# our peers will now all belong to the group, 'myApp'
os.environ['NET_GROUP'] = 'myApp'

# net imports
import net


@net.event("myEvent")  # <- this can be any value.
def something_happened(*args, **kwargs):
    return args, kwargs


# A subscription allows you to connect to an event on another peer. This does
# not need to always be a hub and peers can subscribe to events on any other
# peer the same way we did here minus the "hubs_only=True"
@net.subscribe("myEvent", hubs_only=True, on_host=True)
def handle_something_happened(message):
    """
    Simply print what happened.
    """
    print(message)