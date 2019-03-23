# net imports
import net

# This version of the peer will run the latest version of the
import app_v2


if __name__ == '__main__':

    all_app_peers = net.peers(groups=['app_v1', 'app_v2'], on_host=True)
    # First we need to grab the to running peers on our local host in both the
    # app_v1 and app_v2 groups. This will give us a dict laid out as follows.
    # {
    #       'peers': {
    #           peer1_id: info,
    #           peer2_id: info,
    #       },
    #       app_v1: [
    #           peer1_id
    #       ],
    #       app_v2: [
    #           peer2_id
    #       ]
    # }
    # This will allow us to better access the peers. You can grab a peer
    # directly of the dictionary OR get the group which has a list of all the
    # peer_ids that belong to it. Then use that list of peers to gran the
    # information.

    app_v1_peer = all_app_peers['app_v1'][0]
    # Lets grab the first peer that is using the app_v1 api and execute our
    # tagged function

    response = app_v2.connected_function("My Message!", peer=app_v1_peer)
    print(response)
    # This will result with "My Message! Version 1". Which shows that this new
    # api_v2 can still request a tagged version on an older platform.

    app_v2_peer = all_app_peers['app_v2'][0]
    # Lets grab the first peer that is using the app_v2 api and execute our
    # tagged function

    response = app_v2.connected_function("My Message!", peer=app_v2_peer)
    print(response)
    # This will result with "My Message! Version 2". Which is the latest version
    # of the api.
