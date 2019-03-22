# -*- coding: utf-8 -*-
"""
Subscribe Module
----------------

Contains the subscribe and event decorators and should have nothing else.
"""

__all__ = [
    'subscribe'
]

# std imports
from functools import wraps

# package imports
import net


def subscribe(event, peers=None):
    """
    Subscribe to an event on another peer or set of peers. When the peer
    triggers an event using a function decorated with the ``net.subscription``,
    the peer will take the result and pass it to this function. By default, this
    will subscribe to all peers with a matching event. You can also manually
    filter the peers by selectively passing in only the peers you want to
    subscribe to using the ``peers`` keyword argument. This will only subscribe
    to that even on those peers.

    Subscribe to "some_event" on a group1 peers only.

    .. code-block:: python

        group1_peers = net.get_peers(groups=['group1'])

        @net.subscribe("some_event", group1_peers)
        def your_function(subscription_args, subscription_kwarg=None):
            return some_value

    Subscribe to "some_event" on a single peer.

    .. code-block:: python

        peer = net.get_peers()[0]

        @net.subscribe("some_event", peer)
        def your_function(subscription_args, subscription_kwarg=None):
            return some_value

    Subscribe to "some_event" on all peers.

    .. code-block:: python

        @net.subscribe("some_event")
        def your_function(subscription_args, subscription_kwarg=None):
            return some_value

    """
    # handle peers arg
    if not peers:
        peers = net.get_peers()
    else:
        if not isinstance(peers, (list, tuple)):
            peers = [peers]

    def wrapper(func):

        # build the connection id
        connection = net.Peer().register_connection(func)
        local_peer_id = net.Peer().id

        # loop over all the requested peers
        for peer in peers:
            net.subscription_handler(
                event,
                str(local_peer_id),
                str(connection),
                peer=peer
            )
        return func
    return wrapper
