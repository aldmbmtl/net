#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Tests for `net` package."""
import pytest

import net


@pytest.fixture(scope="module")
def peers():
    """
    Set up the peers for testing.
    """
    master = net.Peer()
    yield master, master.__class__(test=True)


def test_peer_construct(peers):
    """
    Construct and connect 2 peer servers.
    """
    master, slave = peers
    assert master.port != slave.port
    assert slave.ping(master.port, master.host) is True
    assert master.ping(slave.port, slave.host) is True


def test_connect_decorator():
    """
    Test the connect decorator
    """
    pass