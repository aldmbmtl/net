# -*- coding: utf-8 -*-
"""
Handler Module
--------------

Contains the peer handler and should have nothing else.
"""

__all__ = [
    'THREAD_LIMIT',
    'HOST_NAME',
    'SUBNET_IP',
    'SUBNET_MASK',
    'SUBNET_CIDR',
    'PORT_RANGE',
    'PORT_START',
    'LOGGER',
    'DEV_MODE',
    'GROUP',
    'IS_SERVER'
]

# std imports
import os
import socket
from logging import getLogger, StreamHandler, Formatter, DEBUG

# thread limit
THREAD_LIMIT = int(os.environ.setdefault("NET_THREAD_LIMIT", "5"))

# networking
HOST_NAME = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0] + '.0'
SUBNET_IP = os.environ.setdefault("NET_SUBNET", HOST_NAME)
SUBNET_MASK = os.environ.setdefault("NET_SUBNET_MASK", '25')
SUBNET_CIDR = "{0}/{1}".format(SUBNET_IP, SUBNET_MASK)
PORT_START = int(os.environ.setdefault("NET_PORT", "3010"))
PORT_RANGE = int(os.environ.setdefault("NET_PORT_RANGE", "10"))

# peer configuration
GROUP = str(os.environ.get("NET_GROUP"))
IS_SERVER = os.environ.get("NET_IS_SERVER") is not None


# handle development environment
DEV_MODE = os.environ.get("HFX_DEV")

# configure logger
LOGGER = getLogger('net')

LOGGER_HANDLER = StreamHandler()
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER_HANDLER.setFormatter(Formatter("%(name)s:%(levelname)s\t%(message)s"))

if DEV_MODE:
    LOGGER.setLevel(DEBUG)
