# -*- coding: utf-8 -*-
"""
Connect Module
--------------

Contains the connect decorator and should have nothing else.
"""

__all__ = [
    'connect'
]

# std imports
from functools import wraps

# package imports
from net import LOGGER

# 3rd party
from termcolor import colored

# package imports
from .peer import Peer, _Peer


# noinspection PyShadowingNames
def connect(tag=None):
    """
    Registers a function as a connection. This will be tagged and registered
    with the Peer server. The tag is a base64 encoded path to the function or
    can be manually tagged with the tag parameter.

    .. code-block:: python

        @net.connect()
        def your_function(some_value):
            return some_value

    """
    def wrapper(func):
        # register the function with the peer handler
        connection_name = _Peer.register_connection(tag if tag else func)

        @wraps(func)
        def interface(*args, **kwargs):
            # grab the local peer
            peer = Peer()

            # execute the function as is if this is being run by the local peer
            if not kwargs.get('peer'):
                LOGGER.debug("{0} execution on {1}".format(
                    colored("Local", 'green', attrs=['bold']),
                    colored(str(peer.friendly_id), 'magenta'))
                )

                # run the target connection locally
                response = func(*args, **kwargs)

                # This is to simulate the Peer environment as far as processing
                # the flags
                processor = peer.process_flags(response)
                if processor:
                    terminate = processor(connection_name, peer.friendly_id)
                    if terminate:
                        return terminate

                # this response should be the same as if it was remote. But just
                # in the context of the local host. This means I must encode the
                # response and then decode it which is what the remote host will
                # do.
                response = peer.encode(response)
                return peer.decode(response)

            encoded_address = kwargs.get('peer')
            remote_peer_address = str(peer.decode_id(encoded_address))
            LOGGER.debug("{0} execution on {1}".format(
                colored("Remote", 'blue', attrs=['bold']),
                colored(remote_peer_address, 'magenta'))
            )

            # clean out the peer argument from the kwargs and make request
            response = peer.request(encoded_address, connection_name, args, kwargs)

            # handle error catching
            if isinstance(response, dict):
                if response.get('payload') and response.get('payload') == 'error':
                    # unpack the traceback and raise an exception
                    full_error = "RemoteError\n" + response['traceback']
                    LOGGER.error(full_error)
                    raise Exception(full_error)

            # return the response
            return response
        return interface
    return wrapper
