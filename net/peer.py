# -*- coding: utf-8 -*-

__all__ = [
    'Peer'
]

# std imports
import re
import os
import sys
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

    # utilities
    ID_REGEX = re.compile(r"(?P<host>.+):(?P<port>\d+) -> (?P<group>.+)")

    # store
    CONNECTIONS = {}
    FLAGS = {}

    @staticmethod
    def ports():
        """
        Generator; All ports defined in the environment.
        :return: int
        """
        port_start = int(os.environ.setdefault("NET_PORT", "3010"))
        port_range = port_start + int(os.environ.setdefault("NET_PORT_RANGE", "40"))

        # loop over ports
        for port in range(port_start, port_range):
            yield port

    @staticmethod
    def ping(port, host=socket.gethostname()):
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
    def generate_id(port, host, group):
        """
        Generate a peers id.
        :param port:
        :param host:
        :param group:
        :return:
        """
        return base64.b64encode(
            '{host}:{port} -> {group}'.format(
                host=socket.gethostname() if not host else host,
                port=port,
                group=group,
            ).encode('ascii')
        )

    @classmethod
    def decode_id(cls, id):
        """
        Decode a peer id
        :param id:
        :return:
        """
        expr = cls.ID_REGEX.match(base64.b64decode(id).decode('ascii')).groupdict()

        return {
            'group': expr['group'],
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
                except (OSError, ConnectionRefusedError):
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
    def register_connection(cls, connection):
        """
        Registers a connection with the global handler.
        Do not use this directly. Instead use the net.connect decorator.

        @net.connect
        def your_function(payload):
            arg1 = payload['argument1']
            ...do something

        @net.connect
        def your_next_function(payload):
            arg1 = payload['argument1']
            ...do something

        :param connection: function
        :return:
        """
        connections_name = cls.build_connection_name(connection)

        # add the connection to the connection registry.
        if connections_name in cls.CONNECTIONS:
            warning("Redefining a connection handler. Be aware, this could cause unexpected results.")
        cls.CONNECTIONS[connections_name] = connection

        return connections_name

    @classmethod
    def register_flag(cls, flag, handler):
        """
        Registers a flag with the peer server. Flags are simple responses that can trigger error handling or logging.
        Do not use this directly. Instead use the net.flag decorator.

        @net.flag("SOME_ERROR")
        def your_next_function(peer, connection):
            raise SomeError("This failed because {0} failed on the other peer.".format(connection))

        :param flag: payload
        :param handler: function
        :return:
        """

        flag = base64.b64encode(flag.encode('ascii'))

        if flag in cls.FLAGS:
            warning("Redefining a flag handler. Be aware, this could cause unexpected results.")

        cls.FLAGS[flag] = handler

        return flag

    @classmethod
    def get_flag(cls, flag):
        """
        Get a flags id.
        :param flag:
        :return:
        """
        encoded = base64.b64encode(flag.encode('ascii'))

        # validate the flag requested
        if encoded not in cls.FLAGS:
            raise Exception("Invalid Flag requested.")

        return encoded

    def __init__(self, launch=True, test=False, group=None):

        # mask with singleton catch unless being tested
        if SINGLETON and not test:
            raise RuntimeError(
                "Can not create a new peer in without shutting down the previous one. Please use net.Peer() instead."
            )

        # find port
        self._host = socket.gethostname()
        self._port = self.scan_for_port()
        self._group = str(os.environ.get('NET_GROUP') if not group else group)

        # handle threading
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True

        # launch the peer
        if launch:
            self.launch()

    @property
    def group(self):
        return self._group

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
        return self.generate_id(self.port, self.host, self.group)

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

    def request(self, peer, connection, *args, **kwargs):
        """
        Request an action and response from a peer.
        :param peer: base64 encoded peer id
        :param connection: the target connection id to run
        :param kwargs: keyword arguments to pass to the target connection (must be json compatible)
        :return:
        """
        # decode
        if not isinstance(peer, tuple):
            expr = self.decode_id(peer)
            peer = (expr['host'], expr['port'])

        # package up the request
        payload = {'connection': connection.decode('ascii'), 'args': args, 'kwargs': kwargs}

        # socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set the time out on the function
        if kwargs.get('time_out'):
            sock.settimeout(kwargs.get('time_out'))

        # connect
        sock.connect(peer)

        # send request
        sock.sendall(PeerHandler.encode(self.id, payload))

        # sock
        raw = sock.recv(1024)

        # handle flags
        if raw in self.FLAGS:
            terminate = self.FLAGS[raw](self, connection, peer)
            if terminate:
                return terminate

        # decode and return final response
        return PeerHandler.decode(raw)


# noinspection PyPep8Naming
def Peer(*args, **kwargs):
    """
    Running Peer server for this instance of python.
    :return: _Peer
    """
    global SINGLETON

    # handle singleton behavior
    if not SINGLETON:
        SINGLETON = _Peer(*args, **kwargs)

    return SINGLETON