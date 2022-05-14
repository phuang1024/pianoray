"""
Global utilities.
"""

import os
import shutil
from pathlib import Path

from . import logger

VERSION = "0.2.3"

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


def strnum(v):
    """
    Returns str(v) if v >= 0 else "n" + str(abs(v))
    Used for getting a filename given frame number.
    """
    return str(v) if v >= 0 else "n" + str(abs(v))


def bounds(v, vmin, vmax):
    """
    Bound v between vmin and vmax.
    """
    return min(max(v, vmin), vmax)

def interp(v, from_range, to_range):
    """
    Like np.interp, except better.
    Can handle v out of from_range, reversed ranges, etc.
    """
    fac = (v-from_range[0]) / (from_range[1]-from_range[0])
    return fac * (to_range[1]-to_range[0]) + to_range[0]
