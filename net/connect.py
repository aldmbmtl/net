# -*- coding: utf-8 -*-

__all__ = [
    'connect'
]

# std imports
from logging import info, error

# package imports
from .peer import Peer, _Peer

# 3rd party
from termcolor import colored


# noinspection PyShadowingNames
def connect(func):
    """
    Register a function as a handler for the peer server.
    """
    # register the function with the peer handler
    connection_name = _Peer.register_connection(func)

    def interface(*args, **kwargs):
        # execute the function as is if this is being run by the local peer
        if kwargs.get('NET_RUN') or not kwargs.get('peer'):
            info(colored("Remote", 'green') + " call.")
            return func(Peer(), *args, **kwargs)


        info(colored("Remote", 'blue') + " call.")
        response = Peer().request(connection=connection_name, **kwargs)

        # handle error catching
        if isinstance(response, dict) and response.get('payload'):
            if response.get('payload') == 'error':
                raise Exception("RemoteError\n" + response['traceback'])

        # return the response
        return response

    return interface