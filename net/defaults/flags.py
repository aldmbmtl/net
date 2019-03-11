# -*- coding: utf-8 -*-

# std imports
import base64

# package imports
from net import flag


# Flags
@flag('NULL')
def null_response(this_peer, connection, peer):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.
    :param this_peer:
    :param connection:
    :param peer:
    :return:
    """
    return 1


# Flags
@flag('INVALID_CONNECTION')
def invalid_connection(this_peer, connection, peer):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.
    :param this_peer:
    :param connection:
    :param peer:
    :return:
    """
    raise Exception(
        "Peer does not have the connection you are requesting.\n\t"
        "Peer: {0}@{1}\n\t"
        "Connection Requested: {2} -> {3}".format(
            peer[0],
            peer[1],
            connection,
            base64.b64decode(connection).decode('ascii')
        )
    )