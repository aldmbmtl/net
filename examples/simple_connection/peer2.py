# net imports
import net

# Importing the application code will automatically launch the peer and begin
# listening for connection requests as well as set up the connection registry.
import app


if __name__ == '__main__':

    all_peers = net.peers(on_host=True)
    # Gets all the peers on the local network. This will return a dictionary
    # where the key is the Peer.id of the peer and value is a dictionary of
    # information about that peer. In this case, we know that both peers are
    # running on the same host so we want to pass in the no_host=True. The
    # result will be the same, but this will be significantly faster since it is
    # not going to be searching the whole network.
    #
    # Example response:
    # {
    #   'peers': {
    #       b'MTkyLjE2OC4yLjI0OjMwMTAgLT4gTm9uZQ==': {
    #           'group': 'None',
    #           'host': '192.168.2.24',
    #           'port': 3010,
    #           'hub': False
    #       },
    #    },
    #   'None': [
    #       b'MTkyLjE2OC4yLjI0OjMwMTAgLT4gTm9uZQ=='
    #   ]
    # }

    target_peer = all_peers['None'][0]
    # since we know there is only one other peer running our application in the
    # "None" group, we can assume it is safe to grab the first key. This will be
    # how net knows where to execute our application. Just a note, by default, a
    # peer that was initialized without a group set in its environment is set to
    # the "None" group.

    app.connected_function("My Message!", peer=target_peer)
    # now we can call our applications function. Since this function is
    # connected through net, we can pass in the keyword argument 'peer' to
    # specify where to execute the function. If you do not specify the peer, it
    # will simply execute the code locally as though it was not connected.
    # Basically just a normal function.

    # Running this will now print "My Message!" on peer1.
