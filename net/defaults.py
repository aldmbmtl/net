# -*- coding: utf-8 -*-

__all__ = [
    'info'
]

from .connect import connect, payload

info_payload = payload(
    name=True,
    host=True,
    application=False
)


@connect(payload=info_payload)
def info(payload):
    """
    Return information about the peer requested.
    :param payload:
    :return:
    """
    print(payload)