# -*- coding: utf-8 -*-
"""
Default Flags
-------------

Prebuilt flags for net. Do not modify.
"""

__all__ = [
    'null_response',
    'invalid_connection'
]

# std imports
import base64

# package imports
from net import flag


# Flags
@flag('NULL')
def null_response(connection, foreign_peer_id):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.

    :param connection: name of the connection requested
    :param foreign_peer_id: The foreign peers friendly_id
    :return: str
    """
    return "NULL"


# Flags
@flag('INVALID_CONNECTION')
def invalid_connection(connection, foreign_peer_id):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.

    :param connection: name of the connection requested
    :param foreign_peer_id: The foreign peers friendly_id
    :return:
    """
    raise Exception(
        "Peer does not have the connection you are requesting.\n\t"
        "Peer: {0}@{1}\n\t"
        "Connection Requested: {2} -> {3}".format(
            foreign_peer_id['host'],
            foreign_peer_id['port'],
            connection,
            base64.b64decode(connection).decode('ascii')
        )
    )
