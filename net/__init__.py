# -*- coding: utf-8 -*-
"""Top-level package for net."""
from __future__ import print_function

__all__ = [
    'connect',
    'flag',
    'Peer',
    'LOGGER',
    'null_response',
    'pass_through',
    'null',
    'info',
    'invalid_connection',
]

# std imports
import os
from logging import getLogger, StreamHandler, Formatter, DEBUG

# development environment
LOGGER = getLogger('net')
LOGGER_HANDLER = StreamHandler()
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER_HANDLER.setFormatter(Formatter("%(name)s:%(levelname)s\t%(message)s"))
if os.environ.get('HFX_DEV'):
    LOGGER.setLevel(DEBUG)
    # basicConfig(level=DEBUG)

__author__ = 'Alex Hatfield'
__email__ = 'alex@hatfieldfx.com'
__version__ = '0.1.0'

from .peer import *
from .flag import *
from .connect import *
from .defaults import *
from .api import *
