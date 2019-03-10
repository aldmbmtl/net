# -*- coding: utf-8 -*-

# std imports
import json
import base64
import traceback
from logging import error
from . import peer

# python 2/3 imports
from .imports import socketserver


class PeerHandler(socketserver.BaseRequestHandler):
    """
    Handles all incoming requests to the applications Peer server. Do not modify or interact with directly.
    """

    CONNECTION_PAYLOADS = {}

    @classmethod
    def payloads(cls):
        return cls.CONNECTION_PAYLOADS

    @classmethod
    def register_connection_payload(cls, name, template):
        """
        Register a type of connection payload. This defines the data payload contract between peers. If you would like
        to create a new type of connection payload, you must define the template of the payload so if can be verified
        before attempting delivery or execution.

        :param name: connection payload name. This is store in the PeerHandler.types["my_type"]
        :param template: dict
        :return:
        """
        if name in cls.CONNECTION_PAYLOADS:
            raise TypeError(
                "{0} is already a registered connection payload. Please choose a different name.".format(name)
            )

        cls.CONNECTION_PAYLOADS[name] = template

    @classmethod
    def validate_connection_payload(cls, payload):
        """
        Validates the payload against the registered template for the defined payload type.
        :param payload:
        :return:
        """
        print(payload['payload'])

    @classmethod
    def decode(cls, byte_string):
        """
        Decode a byte string sent from a peer.
        :param byte_string:
        :return:
        """
        payload = json.loads(str(base64.b64decode(byte_string), 'ascii'))
        cls.validate_connection_payload(payload)
        return payload

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
        cls.validate_connection_payload(obj)
        return base64.b64encode(bytes(json.dumps(obj), 'ascii'))

    def handle(self):
        """
        Handles all incoming requests to the server.
        :return:
        """
        raw = self.request.recv(1024)

        # if there is no data, bail and don't respond
        if not raw:
            return

        # convert from json
        try:
            data = self.decode(raw)

            if not data:
                return

            if data['payload'] == 'none':
                packet = {'payload': 'ping'}
                payload = self.encode(self.server.id, packet)
                self.request.sendall(payload)

        except (json.decoder.JSONDecodeError, TypeError) as e:
            error(e)
            packet = {
                'payload': 'error',
                'traceback': traceback.format_exc()
            }
            payload = self.encode(self.server.id, packet)
            self.request.sendall(payload)
