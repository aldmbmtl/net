#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Tests for `net` package."""

# testing
import pytest

# package
import net


@pytest.fixture(scope="module")
def peers():
    """
    Set up the peers for testing.
    """
    net.LOGGER.debug("Test Header")

    master = net.Peer()
    slave = master.__class__(test=True)

    yield master, slave


def test_peer_construct(peers):
    """
    Construct and connect 2 peer servers.
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    assert master.port != slave.port
    assert slave.ping(master.port, master.host) is True
    assert master.ping(slave.port, slave.host) is True


def test_connect_decorator(peers):
    """
    Test the connect decorator
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    assert net.info() != net.info(peer=slave.id)

    test_cases = [
        # dicts types
        {"testing": "value"}, {"1": 1}, {"1": {"2": 3}},

        # array types
        [1, "1", "1"], (1, 2, 3),

        # strings types
        "This is a string", "",

        # None type
        None,

        # bool types
        True, False,

        # number types
        1.0, 1,
    ]

    # loop over each test case and make sure a remote response equals to a local response.
    for case in test_cases:
        assert net.pass_through(case) == net.pass_through(case, peer=slave.id)


def test_flag_decorator(peers):
    """
    Test the connect decorator
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    # define the testing connection handler
    @net.connect
    def test_response_handler(peer, handler):
        flag = peer.get_flag("TEST")
        return flag

    # should throw an error since the flag is not defined yet
    with pytest.raises(Exception):

        net.LOGGER.disabled = True
        test_response_handler(peer=slave.id)
        net.LOGGER.disabled = False

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
    net.LOGGER.debug("Test Header")

    assert net.get_peers(_test_bypass_threading=True) == net.get_peers()


def test_none_threaded_api():
    """
    Test api functions
    """
    net.LOGGER.debug("Test Header")

    assert len(net.get_peers(_test_bypass_threading=True)) == 2


def test_threaded_api():
    """
    Test api functions
    """
    net.LOGGER.debug("Test Header")

    assert len(net.get_peers()) == 2
