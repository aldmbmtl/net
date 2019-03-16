# -*- coding: utf-8 -*-

# package imports
from net import connect


# basic descriptor
@connect
def info(peer, request, *args, **kwargs):
    """
    Return information about the peer requested.
    :return:
    """
    return peer.friendly_id


# utilities
@connect
def pass_through(peer, request, *args, **kwargs):
    """
    Used for testing, takes your arguments and passes them back for type testing.
    :return:
    """
    if len(args) == 1:
        return args[0]
    return args, kwargs


@connect
def null(peer, request, *args, **kwargs):
    """
    Return a null response flag
    :return:
    """
    return peer.get_flag("NULL")