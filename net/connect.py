# -*- coding: utf-8 -*-

# package imports
from .peer import _Peer


def connect(func):
    """
    Register a function as a handler for the peer server.
    """
    # register the function with the peer handler
    _Peer.register_connection(func)

    def net_interface(*args, **kwargs):
        # determine if this is a remote request or local
        handler = kwargs.get("_net_handler")

        print(_Peer.CONNECTIONS)

        if handler:
            print("this is a remote call!")
        else:
            print("this is a local call!")

        return func(*args, **kwargs)

    return net_interface