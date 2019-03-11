# -*- coding: utf-8 -*-

# package imports
from net import connect


@connect
def info(peer, request, *args, **kwargs):
    """
    Return information about the peer requested.
    :return:
    """
    return request.encode(
        peer.id,
        peer.friendly_id
    )
