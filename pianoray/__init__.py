import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from . import effects
from . import render
from . import utils

__version__ = utils.VERSION
