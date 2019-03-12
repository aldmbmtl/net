# -*- coding: utf-8 -*-

__all__ = [
    'get_remote_peers'
]

# std imports
import os
import socket

# third party
import netaddr

# package imports
import net

# local imports
from net.imports import ConnectionRefusedError


DEFAULT = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0] + '.0'
SUBNET_IP = os.environ.get("SUBNET") if os.environ.get("SUBNET") else DEFAULT
SUBNET_MASK = os.environ.get("SUBNET_MASK") if os.environ.get("SUBNET_MASK") else '25'
SUBNET_CIDR = "{0}/{1}".format(SUBNET_IP, SUBNET_MASK)


def get_remote_peers(groups=[]):
    """
    Get a list of all valid remote peers.

    :param groups: List of groups
    :return: List of peer addresses
    """
    total_pings = 0
    found_peers = []

    # get this peer for pinging
    peer = net.Peer()

    # create subnet
    network = netaddr.IPNetwork(SUBNET_CIDR)

    # groups
    if not groups:
        groups = [peer.group]

    # loop over all the addresses
    for address in network:

        # loop over ports
        for port in peer.ports():

            # loop over ports
            for group in groups:

                # generate the peer
                foreign_peer_id = peer.generate_id(port, address, group)

                try:
                    # ping the peer and if it responds with the proper info, register it
                    net.info(peer=foreign_peer_id, time_out=0.005)
                    found_peers.append(foreign_peer_id)
                except (PermissionError, ConnectionRefusedError, OSError):
                    pass

                total_pings += 1

    print("Total pings: {0}".format(total_pings))
    print("Found peers: {0}".format(len(found_peers)))