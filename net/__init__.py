# -*- coding: utf-8 -*-

"""Top-level package for net."""
from __future__ import print_function

__author__ = """Alex Hatfield"""
__email__ = 'alex@hatfieldfx.com'
__version__ = '0.1.0'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .peer import Peer