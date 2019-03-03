# -*- coding: utf-8 -*-
# std imports
import os
import socket
from logging import debug

# python version handling
try:
    # python 2
    import SocketServer as socketserver
    from socket import error as ConnectionRefusedError
except ImportError:
    # python 3
    import socketserver

# third party
import termcolor


# globals
SINGLETON = None


class PeerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass


# noinspection PyPep8Naming
class _peer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self):
        # mask with singleton catch
        if SINGLETON:
            raise RuntimeError(
                "Can not create a new peer in without shutting down the previous one. Please use net.Peer() instead."
            )

        # find port
        self.port = self.scan_for_port()
        self.host = 'localhost'

        super(_peer, self).__init__((self.host, self.port), PeerHandler)

    @staticmethod
    def ping(port, host='localhost'):
        """
        Ping a port and check if it is alive or open.

        :param port: required port to hit
        :param host: host address default is 'localhost'
        :return:
        """

        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            interface.connect((host, port))
            return True
        except ConnectionRefusedError:
            return False

    @classmethod
    def scan_for_port(cls):
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

        debug("Scanning {} ports for open port...".format(port_range - port))
        while port <= port_range:

            # ping the local host ports
            if not cls.ping(port):
                debug("Found Port: {}".format(termcolor.colored(port, "green")))
                break

            port += 1

        # throw error if there is no open port
        if port > port_range:
            raise ValueError("No open port found between {} - {}".format(port, port_range))

        # return found port
        return port


def Peer():
    """
    Running Peer server for this instance of python.
    :return: _peer
    """
    global SINGLETON

    # handle singleton behavior
    if not SINGLETON:
        SINGLETON = _peer()

    return SINGLETON