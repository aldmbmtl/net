# -*- coding: utf-8 -*-

# package imports
from net import connect


@connect
def info(request, *args, **kwargs):
    """
    Return information about the peer requested.
    :return:
    """
    return request.encode(
        request.server.id,
        request.server.friendly_id
    )
