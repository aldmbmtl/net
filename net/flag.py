# -*- coding: utf-8 -*-

__all__ = [
    'flag'
]

# package imports
from .peer import Peer


def flag(name):
    """
    Register a function as a flag handler for the peer server.

    :param name:
    """
    def registry(func):
        def handler(*args, **kwargs):
            return func(*args, **kwargs)

        peer = Peer()

        # register the function with the peer handler
        peer.register_flag(name, handler)

        return handler
    return registry