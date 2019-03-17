# -*- coding: utf-8 -*-

__all__ = [
    'info',
    'pass_through',
    'null'
]

# package imports
from net import connect, Peer


# basic descriptor
@connect
def info(*args, **kwargs):
    """
    Return information about the peer requested.

    :return: peer.friendly_id
    """
    return Peer().friendly_id


# utilities
@connect
def pass_through(*args, **kwargs):
    """
    Used for testing, takes your arguments and passes them back for type testing.

    :return: *args, **kwargs
    """
    if len(args) == 1:
        return args[0]
    return args, kwargs


@connect
def null(*args, **kwargs):
    """
    Return a null response flag

    :return: NULL Flag
    """
    return Peer().get_flag("NULL")