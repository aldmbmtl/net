# -*- coding: utf-8 -*-
"""
api module
----------

Contains the general network interactions for net.
"""

__all__ = [
    'get_peers',
    'find_peers_in_block'
]

# std imports
import os
import math
import socket
import struct
import threading

# package imports
import net

# local imports
from net.imports import ConnectionRefusedError, PermissionError


# host name
DEFAULT = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0] + '.0'

# thread limit
THREAD_LIMIT = os.environ.get("NETWORK_THREAD_LIMIT")
if not THREAD_LIMIT:
    THREAD_LIMIT = 5

# subnet IP
SUBNET_IP = os.environ.get("SUBNET")
if not SUBNET_IP:
    SUBNET_IP = DEFAULT

# subnet masking
SUBNET_MASK = os.environ.get("SUBNET_MASK")
if not SUBNET_MASK:
    SUBNET_MASK = '25'

# subnet CIDR block
SUBNET_CIDR = "{0}/{1}".format(SUBNET_IP, SUBNET_MASK)

# threading
LOCK = threading.Lock()


def generate_network(ip, cidr):
    """
    Generate a set of ip addresses bases on the cidr network passed

    :param ip:
    :param cidr:
    :return: list of ips
    """
    host_bits = 32 - int(cidr)
    i = struct.unpack('>I', socket.inet_aton(ip))[0]
    start = (i >> host_bits) << host_bits
    end = start | (1 << host_bits)

    return [
        socket.inet_ntoa(struct.pack('>I', address)) for address in range(start, end)
    ]


def find_peers_in_block(ips, groups=[], _shared_array=None):
    """
    Sniffs out peers in the defined group based on the list of ip's

    :param ips: list of ip addresses
    :param groups: the list of groups you'd like to filter with. Defaults to the
     same as the current peer.
    :return: List of peer addresses
    """
    peers = []

    if not groups:
        groups = [net.Peer().group]

    # loop over all the addresses
    for address in ips:

        # loop over ports
        for port in net.Peer().ports():

            # loop over ports
            for group in groups:

                # generate the peer
                foreign_peer_id = net.Peer().generate_id(port, address, group)

                try:
                    # ping the peer and if it responds with the proper info,
                    # register it. Shut off the logger for this so we dont spam
                    # the console.

                    net.LOGGER.disabled = True
                    net.info(peer=foreign_peer_id, time_out=0.005)
                    net.LOGGER.disabled = False

                    peers.append(foreign_peer_id)
                except (PermissionError, ConnectionRefusedError, OSError):
                    net.LOGGER.disabled = False

    if _shared_array is not None:

        LOCK.acquire()
        _shared_array.extend(peers)
        LOCK.release()

    return peers


def get_peers(groups=None, _test_bypass_threading=False):
    """
    Get a list of all valid remote peers.

    :param groups: List of groups
    :return: List of peer addresses
    """
    peers = []

    # get this peer for pinging
    peer = net.Peer()

    # groups
    if not groups:
        groups = [peer.group]

    # create subnet
    network = generate_network(ip=SUBNET_IP, cidr=SUBNET_MASK)

    # logging help
    total_hosts = len(network)
    total_ports = len(peer.ports())
    total_threads = int(THREAD_LIMIT)
    net.LOGGER.debug(
        "Calculated network sweep: {0} hosts X {1} ports = {2} pings".format(
            total_hosts, total_ports, total_hosts * total_ports
        )
    )

    # skip the threading integration if the environment does not call for it.
    if total_threads <= 0 or _test_bypass_threading:
        return find_peers_in_block(network, groups)

    # calculate thread chunk
    thread_chunks = int(math.ceil(total_hosts/total_threads))

    # loop over and spawn threads
    start = 0
    threads = []

    for chunk in range(0, total_threads):
        end = start + thread_chunks

        # spawn thread with network chunk calculated.
        thread = threading.Thread(
            target=find_peers_in_block,
            args=(network[start:end], groups, peers)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

        start = end

    # wait for all worker threads to finish
    for thread in threads:
        thread.join()

    return peers
