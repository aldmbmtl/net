#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Tests for `net` package."""

# std imports
from logging import info

# testing
import pytest

# package
import net


@pytest.fixture(scope="module")
def peers():
    """
    Set up the peers for testing.
    """
    master = net.Peer()
    slave = master.__class__(test=True)
    yield master, slave


def test_peer_construct(peers):
    """
    Construct and connect 2 peer servers.
    """
    master, slave = peers

    assert master.port != slave.port
    assert slave.ping(master.port, master.host) is True
    assert master.ping(slave.port, slave.host) is True


def test_connect_decorator(peers):
    """
    Test the connect decorator
    """
    master, slave = peers

    assert net.info() != net.info(peer=slave.id)


def test_flag_decorator(peers):
    """
    Test the connect decorator
    """
    master, slave = peers

    # define the testing connection handler
    @net.connect
    def test_response_handler(peer, handler):
        flag = peer.get_flag("TEST")
        return flag

    # should throw an error since the flag is not defined yet
    with pytest.raises(Exception):
        test_response_handler(peer=slave.id)

    # define the missing flag
    @net.flag("TEST")
    def test_flag(this_peer, connection, peer):
        return "TEST"

    # flag is defined and should not fail
    assert test_response_handler(peer=slave.id) == "TEST"


def test_api():
    """
    Test api functions
    """
    assert len([peer for peer in net.get_remote_peers()]) == 2
