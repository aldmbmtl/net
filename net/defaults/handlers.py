# -*- coding: utf-8 -*-

# package imports
from net import connect


@connect
def info(peer, *args, **kwargs):
    """
    Return information about the peer requested.
    :return:
    """
    print(peer.friendly_id)
    return args, kwargs