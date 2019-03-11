# -*- coding: utf-8 -*-

__all__ = [
    'connect'
]

# std imports
from logging import info, error

# package imports
from .peer import Peer, _Peer, PeerHandler

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
        if not kwargs.get('peer'):
            info("{0} execution on {1}".format(
                colored("Local", 'green', attrs=['bold']), colored(str(Peer().friendly_id), 'magenta'))
            )
            return PeerHandler.decode(
                func(Peer(), PeerHandler, *args, **kwargs)
            )

        # grab the local peer
        peer = Peer()
        info("{0} execution on {1}".format(
            colored("Remote", 'blue', attrs=['bold']), colored(str(peer.decode_id(kwargs.get('peer'))), 'magenta'))
        )

        # make request
        response = peer.request(connection=connection_name, **kwargs)

        # handle error catching
        if isinstance(response, dict) and response.get('payload'):
            if response.get('payload') == 'error':
                raise Exception("RemoteError\n" + response['traceback'])

        # return the response
        return response

    return interface