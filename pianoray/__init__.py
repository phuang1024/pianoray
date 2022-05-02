"""
PianoRay module.
"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
del os

from . import effects
from . import render
from . import utils

from .api import *

__version__ = utils.VERSION
