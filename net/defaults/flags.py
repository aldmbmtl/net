# -*- coding: utf-8 -*-
"""
Default Flags
-------------

Prebuilt flags for net. Do not modify.
"""

# std imports
import base64

# package imports
import net

__all__ = [
    'null_response',
    'invalid_connection'
]


# Flags
@net.flag('NULL')
def null_response(connection, foreign_peer_id):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.

    :param connection: name of the connection requested
    :param foreign_peer_id: The foreign peers friendly_id
    :return: str
    """
    return "NULL"


# Flags
@net.flag('INVALID_CONNECTION')
def invalid_connection(connection, foreign_peer_id):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.

    :param connection: name of the connection requested
    :param foreign_peer_id: The foreign peers friendly_id
    :return:
    """
    location = "Unknown"
    if not isinstance(connection, str):
        try:
            location = base64.b64decode(connection).decode('ascii')
        except TypeError:
            pass

    raise Exception(
        "Peer does not have the connection you are requesting.\n\t"
        "Peer: {0}@{1}\n\t"
        "Registered Connections: \n\t\t{4}\n\t"
        "Connection Requested: {2} -> {3}".format(
            foreign_peer_id['host'],
            foreign_peer_id['port'],
            connection,
            location,
            '\n\t\t'.join([str(connection) for connection in net.Peer().CONNECTIONS.keys()])
        )
    )
