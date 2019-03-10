# -*- coding: utf-8 -*-

__all__ = [
    'connect',
    'payload'
]

# std imports
import json
from base64 import b64encode, b64decode

# package imports
from .peer import Peer


# noinspection PyShadowingNames
def connect(payload):
    """
    Register a function as a handler for the peer server.

    :param payload:
    """
    def registry(func):
        peer = Peer()

        # register the function with the peer handler
        connection_name = peer.register_connection(func, payload)

        # get the raw payload requirements as a dict
        contract = json.loads(str(b64decode(payload), 'ascii'))

        def interface(*args, **kwargs):
            # execute the function as is if this is being run by the local peer
            if kwargs.get('NET_RUN'):

                # validate the contract
                for key in contract.keys():
                    value = contract[key]
                    if value and key not in kwargs:
                        keys = '\n\t'.join(
                            [key + ' (required)' if contract[key] else key + ' (optional)' for key in contract.keys()]
                        )
                        raise Exception(
                            "Invalid payload passed to peer."
                            "\n\t{0}".format(keys)
                        )

                return func(*args, **kwargs)

            # catch requests with no target
            if not kwargs.get('peer'):
                raise Exception(
                    "You must define the peer you want this function to run on.\n\t"
                    "Example: {0}(peer={1})".format(func.__name__, peer.id)
                )

            peer.request(peer=kwargs.get('peer'), connection=connection_name, **kwargs)

        return interface
    return registry


def payload(**kwargs):
    """
    TODO: Create doc for this. I know what it is but having trouble describing it.

    :param kwargs:
    :return:
    """
    return b64encode(bytes(json.dumps(kwargs, sort_keys=True), 'ascii'))