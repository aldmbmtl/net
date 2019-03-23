# imports
import net


@net.connect()
def connected_function(message):
    """
    This will simply print the message passed on the local peer.
    """
    print(message)