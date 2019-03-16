# -*- coding: utf-8 -*-

__all__ = [
    'PeerHandler',
]

# std imports
import json
import base64
import traceback

# python 2/3 imports
from .imports import socketserver

# package imports
import net


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
            byte_string = base64.b64decode(byte_string).decode('ascii')
            byte_string = json.loads(byte_string)
        except (Exception, json.JSONDecodeError) as e:
            net.LOGGER.debug(byte_string)
            net.LOGGER.debug(e)
            net.LOGGER.debug(traceback.format_exc())

        # if the connection returns data that is not prepackaged as a JSON object, return
        # the raw response as it originally was returned.
        if isinstance(byte_string, dict) and 'raw' in byte_string:
            return byte_string['raw']

        return byte_string

    @classmethod
    def encode(cls, obj):
        """
        Encode an object for delivery.
        :param obj:
        :return:
        """
        if not isinstance(obj, dict):
            try:
                if obj in net.Peer().FLAGS:
                    return obj
            except TypeError:
                pass
            obj = {'raw': obj}

        # tag with the peer
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
            response = self.encode(connection(self.server, self, *data['args'], **data['kwargs']))
            self.request.sendall(response)

        except Exception as e:
            net.LOGGER.error(e)
            net.LOGGER.error(traceback.format_exc())
            packet = {
                'payload': 'error',
                'traceback': traceback.format_exc()
            }
            payload = self.encode(packet)
            self.request.sendall(payload)
