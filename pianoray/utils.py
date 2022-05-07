"""
Global utilities.
"""

import os
import shutil
from pathlib import Path

from . import logger

VERSION = "0.2.1"

ROOT = Path(__file__).absolute().parent

FFMPEG = shutil.which("ffmpeg")
GCC = shutil.which("g++")
if FFMPEG is None:
    logger.warn("No FFmpeg.")
if GCC is None:
    logger.warn("No g++.")


def forever():
    """
    Generator for indefinite tqdm progressbar.
    """
    while True:
        yield


def bounds(v, vmin, vmax):
    """
    Bound v between vmin and vmax.
    """
    return min(max(v, vmin), vmax)
