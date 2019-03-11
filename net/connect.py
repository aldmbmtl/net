# -*- coding: utf-8 -*-

__all__ = [
    'connect'
]

# package imports
from .peer import Peer


# noinspection PyShadowingNames
def connect(func):
    """
    Register a function as a handler for the peer server.
    """
    peer = Peer()

    # register the function with the peer handler
    connection_name = peer.register_connection(func)

    def interface(*args, **kwargs):
        # execute the function as is if this is being run by the local peer
        if kwargs.get('NET_RUN') or not kwargs.get('peer'):
            return func(*args, **kwargs)
        return peer.request(connection=connection_name, **kwargs)
    return interface