# -*- coding: utf-8 -*-
"""
Default Connected Handlers
--------------------------

Prebuilt connected handlers for net. Do not modify.
"""

__all__ = [
    'info',
    'pass_through',
    'null',
    'subscription_handler'
]

# package imports
from net import connect, Peer


# basic descriptor
@connect()
def info(*args, **kwargs):
    """
    Return information about the peer requested.

    :return: peer.friendly_id
    """
    return Peer().friendly_id


# utilities
@connect()
def pass_through(*args, **kwargs):
    """
    Used for testing, takes your arguments and passes them back for type testing.

    :return: *args, **kwargs
    """
    if len(args) == 1:
        return args[0]
    return args, kwargs


@connect()
def null(*args, **kwargs):
    """
    Return a null response flag

    :return: NULL Flag
    """
    return Peer().get_flag("NULL")


@connect()
def subscription_handler(event, peer, connection):
    """
    Will register the incoming peer and connection with the local peers
    subscription of the event passed. This is for internal use only.

    :param event: event id
    :param peer: foreign peer id
    :param connection: connection id
    """
    peer = str(peer.split("'")[1]).encode('ascii')
    connection = str(connection.split("'")[1]).encode('ascii')
    Peer().register_subscriber(event, peer, connection)