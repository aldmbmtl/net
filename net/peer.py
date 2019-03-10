# -*- coding: utf-8 -*-

# std imports
import re
import os
import sys
import json
import socket
import base64
import threading
from logging import debug, warning

# third party
import termcolor

# package imports
from .handler import PeerHandler
from .imports import socketserver, ConnectionRefusedError


# globals
SINGLETON = None


# noinspection PyMissingConstructor
class _Peer(socketserver.ThreadingMixIn, socketserver.TCPServer, object):  # adding in object for 2.7 support

    CONNECTIONS = {}
    REMOTE_CONNECTIONS = {}
    ID_REGEX = re.compile(r"(?P<host>.+):(?P<port>\d+) -> (?P<app>.+)")

    @staticmethod
    def ping(port, host='localhost'):
        """
        Ping a port and check if it is alive or open.

        :param port: required port to hit
        :param host: host address default is 'localhost'
        :return:
        """

        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interface.settimeout(0.25)
        try:
            interface.connect((host, port))
            return True
        except ConnectionRefusedError:
            return False

    @staticmethod
    def generate_id(port, host):
        """
        Generate a peers id.
        :param port:
        :param host:
        :return:
        """
        return base64.b64encode(
            '{host}:{port} -> {exe}'.format(
                host=socket.gethostname() if not host else host,
                port=port,
                exe=sys.executable
            ).encode('ascii')
        )

    @classmethod
    def decode_id(cls, id):
        """
        Decode a peer id
        :param id:
        :return:
        """
        expr = cls.ID_REGEX.fullmatch(str(base64.b64decode(id), 'ascii'))

        return {
            'app': expr['app'],
            'host': expr['host'],
            'port': int(expr['port'])
        }

    def scan_for_port(self):
        """
        Scan for a free port to bind to. You can override the default port range and search range by setting the
        environment variables NET_PORT NET_PORT_RANGE.

        Port range:
            default 3010-3050

        :return: int
        """
        # cast as int and default to 3010 and 40
        port = int(os.environ.setdefault("NET_PORT", "3010"))
        port_range = port + int(os.environ.setdefault("NET_PORT_RANGE", "40"))

        debug("Scanning {0} ports for open port...".format(port_range - port))
        while port <= port_range:

            # ping the local host ports
            if not self.ping(port):
                try:
                    super(_Peer, self).__init__((self.host, port), PeerHandler)
                    debug("Found Port: {0}".format(termcolor.colored(port, "green")))
                    break
                except OSError:
                    warning("Stale Port: {0}".format(termcolor.colored(port, "yellow")))

            port += 1

        # throw error if there is no open port
        if port > port_range:
            raise ValueError("No open port found between {0} - {1}".format(port, port_range))

        # return found port
        return port

    @classmethod
    def build_connection_name(cls, connection):
        """
        Build a connections full name based on the module/name of the function. This is then encoded in base64 for
        easier delivery between peers.

        :param connection: connection
        :return: base64 encoded str
        """
        return base64.b64encode('{0}.{1}'.format(connection.__module__, connection.__name__).encode('ascii'))

    @classmethod
    def get_connection(cls, connection):
        """
        Get a registered connection. Do not use this directly.
        :param connection:
        :return:
        """
        return cls.register_connection(connection)

    @classmethod
    def register_connection(cls, connection):
        """
        Registers a connection with the global handler.
        Do not use this directly. Instead use the net.connect decorator.

        @net.connect
        def your_function():
            ...

        :param connection: function
        :return:
        """
        connections_name = cls.build_connection_name(connection)

        if connections_name not in cls.CONNECTIONS or cls.CONNECTIONS[connections_name] is not connection:
            cls.CONNECTIONS[connections_name] = connection

        return cls.CONNECTIONS[connections_name]

    def __init__(self, launch=True, test=False):

        # mask with singleton catch unless being tested
        if SINGLETON and not test:
            raise RuntimeError(
                "Can not create a new peer in without shutting down the previous one. Please use net.Peer() instead."
            )

        # find port
        self._host = "localhost"
        self._port = self.scan_for_port()

        # handle threading
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True

        # launch the peer
        if launch:
            self.launch()

    @property
    def port(self):
        """
        Port that the peer is running on.
        :return:
        """
        return self._port

    @property
    def host(self):
        """
        Host that the peer is running on.
        :return:
        """
        return self._host

    @property
    def id(self):
        """
        Get this peers id. This is tethered to the port and the executable path the peer was launched with. This is
        base64 encoded for easier delivery.
        :return:
        """
        return self.generate_id(self.port, self.host)

    @property
    def friendly_id(self, peer_id=None):
        """
        Get the peers id in a friendly displayable way.
        :return:
        """
        if not peer_id:
            peer_id = self.id

        # decode and hand back
        return self.decode_id(peer_id)

    def launch(self):
        """
        Launch the peer. This should only be used if Peer(launch=False). Otherwise this is executed at init.
        :return:
        """
        self._thread.start()

    def request(self, peer, target=None, *args, **kwargs):
        """
        Request an action and response from a peer.
        :param peer: base64 encoded peer id
        :param target: the target connection id to run
        :param args: positional arguments to pass to the target connection (must be json compatible)
        :param kwargs: keyword arguments to pass to the target connection (must be json compatible)
        :return:
        """
        # decode
        if not isinstance(peer, tuple):
            expr = self.decode_id(peer)
            peer = (expr['host'], expr['port'])

        # package up the request
        payload = {
            'payload': 'none',
            'message': None,
            'args': args,
            'kwargs': kwargs
        }

        # socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(peer)

        # send request
        sock.sendall(PeerHandler.encode(self.id, payload))

        # sock
        raw = sock.recv(1024)
        response = PeerHandler.decode(raw)


def Peer(*args, **kwargs):
    """
    Running Peer server for this instance of python.
    :return: _peer
    """
    global SINGLETON

    # handle singleton behavior
    if not SINGLETON:
        SINGLETON = _Peer(*args, **kwargs)

    return SINGLETON