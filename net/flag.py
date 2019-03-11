# -*- coding: utf-8 -*-

__all__ = [
    'flag'
]

# package imports
from .peer import _Peer


def flag(name):
    """
    Register a function as a flag handler for the peer server.

    :param name:
    """
    def registry(func):
        def handler(*args, **kwargs):
            return func(*args, **kwargs)

        # register the function with the peer handler
        _Peer.register_flag(name, handler)

        return handler
    return registry