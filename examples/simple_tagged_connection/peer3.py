# net imports
import net

# This version of the peer will run the latest version of the
import app_v2


if __name__ == '__main__':

    all_app_peers = net.peers(groups=['app_v1', 'app_v2'], on_host=True)
    # First we need to grab the to running peers on our local host in both the
    # app_v1 and app_v2 groups.

    app_v1_peer = net.peer_group('app_v1')[0]
    # Lets grab the first peer that is using the app_v1 api and execute our
    # tagged function

    response = app_v1_peer.connected_function("My Message!")
    print(response)
    # This will result with "My Message! Version 1". Which shows that this new
    # api_v2 can still request a tagged version on an older platform.

    app_v2_peer = net.peer_group('app_v2')[0]
    # Lets grab the first peer that is using the app_v2 api and execute our
    # tagged function

    response = app_v2_peer.connected_function("My Message!")
    print(response)
    # This will result with "My Message! Version 2". Which is the latest version
    # of the api.
