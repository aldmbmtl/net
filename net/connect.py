# -*- coding: utf-8 -*-

__all__ = [
    'connect'
]

# package imports
from .peer import Peer


def connect(func):
    """
    Register a function as a handler for the peer server.
    """
    peer = Peer()

    # register the function with the peer handler
    peer.register_connection(func)

    def net_interface(*args, **kwargs):
        # determine if this is a remote request or local
        handler = kwargs.get("_net_handler")

        print(peer.CONNECTIONS)

        if handler:
            print("this is a remote call!")
        else:
            print("this is a local call!")

        return func(*args, **kwargs)

    return net_interface