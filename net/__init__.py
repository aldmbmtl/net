# -*- coding: utf-8 -*-
"""Top-level package for net."""
from __future__ import print_function

# std imports
import os
from logging import basicConfig, DEBUG

# development environment
if os.environ.get('HFX_DEV'):
    basicConfig(level=DEBUG)

__author__ = 'Alex Hatfield'
__email__ = 'alex@hatfieldfx.com'
__version__ = '0.1.0'

__all__ = ['connect', 'Peer']

from .peer import Peer
from .connect import connect
from .defaults import *