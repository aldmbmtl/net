# -*- coding: utf-8 -*-

__all__ = [
    'PeerHandler',
]

# std imports
import json
import base64
import traceback
from logging import error

# python 2/3 imports
from .imports import socketserver


class PeerHandler(socketserver.BaseRequestHandler):
    """
    Handles all incoming requests to the applications Peer server. Do not modify or interact with directly.
    """
    @classmethod
    def decode(cls, byte_string):
        """
        Decode a byte string sent from a peer.
        :param byte_string:
        :return:
        """
        try:
            payload = json.loads(base64.b64decode(byte_string))
            return payload
        except Exception as e:
            error(e)
            return byte_string

    @classmethod
    def encode(cls, peer_id, obj):
        """
        Encode an object for delivery.
        :param peer_id: str
        :param obj:
        :return:
        """
        # tag with the peer
        obj['peer'] = str(peer_id)
        return base64.b64encode(json.dumps(obj).encode('ascii'))

    # noinspection PyPep8Naming
    def handle(self):
        """
        Handles all incoming requests to the server.
        :return:
        """
        raw = self.request.recv(1024)

        # response codes
        NULL = self.server.get_flag('NULL')
        INVALID_CONNECTION = self.server.get_flag('INVALID_CONNECTION')

        # if there is no data, bail and don't respond
        if not raw:
            self.request.sendall(NULL)
            return

        # convert from json
        try:
            data = self.decode(raw)

            # skip if there is no data in the request
            if not data:
                self.request.sendall(NULL)
                return

            # pull in the connection registered on this peer.
            connection = self.server.CONNECTIONS.get(data['connection'].encode('ascii'))

            # throw invalid if the connection doesn't exist on this peer.
            if not connection:
                self.request.sendall(INVALID_CONNECTION)
                return

            # execute the connection handler and send back
            response = connection(self, *data['args'], **data['kwargs'])
            self.request.sendall(response)

        except Exception as e:
            error(e)
            packet = {
                'payload': 'error',
                'traceback': traceback.format_exc()
            }
            payload = self.encode(self.server.id, packet)
            self.request.sendall(payload)
