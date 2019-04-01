# net imports
import net

# Importing the application code will automatically launch the peer and begin
# listening for connection requests as well as set up the connection registry.
import app


if __name__ == '__main__':
    target_peer = net.peer_group(on_host=True)[0]
    # since we know there is only one other peer running our application in the
    # "None" group, we can assume it is safe to grab the first key. This will be
    # how net knows where to execute our application. Just a note, by default, a
    # peer that was initialized without a group set in its environment is set to
    # the "None" group.

    target_peer.connected_function("My Message!")
    # now we can call our applications function. Since this function is
    # connected through net, we can pass in the keyword argument 'peer' to
    # specify where to execute the function. If you do not specify the peer, it
    # will simply execute the code locally as though it was not connected.
    # Basically just a normal function.

    # Running this will now print "My Message!" on peer1.
