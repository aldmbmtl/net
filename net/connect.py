# -*- coding: utf-8 -*-

__all__ = [
    'connect'
]

# package imports
from .peer import Peer, _Peer, PeerHandler

# 3rd party
from termcolor import colored

# package imports
from net import LOGGER


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
            LOGGER.debug("{0} execution on {1}".format(
                colored("Local", 'green', attrs=['bold']), colored(str(Peer().friendly_id), 'magenta'))
            )

            # run the target connection locally
            response = func(Peer(), PeerHandler, *args, **kwargs)

            # This is to simulate the Peer environment as far as processing the flags
            processor = Peer().process_flags(response)
            if processor:
                terminate = processor(Peer(), connection_name, Peer())
                if terminate:
                    return terminate

            # this response should be the same as if it was remote. But just in the context of the local host.
            # This means I must encode the response and then decode it which is what the remote host will do.
            response = PeerHandler.encode(response)
            return PeerHandler.decode(response)

        # grab the local peer
        peer = Peer()
        encoded_address = kwargs.get('peer')
        remote_peer_address = str(peer.decode_id(encoded_address))
        LOGGER.debug("{0} execution on {1}".format(
            colored("Remote", 'blue', attrs=['bold']), colored(remote_peer_address, 'magenta'))
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