#
#  PianoRay
#  Video rendering pipeline with piano visualization.
#  Copyright  PianoRay Authors  2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import ctypes
import os
from math import hypot

import numpy as np

from ...cpp import build_lib, Types
from ...settings import Settings
from ..utils import bounds, key_coords, note_coords

PARENT = os.path.dirname(os.path.abspath(__file__))


def render_blocks(lib: ctypes.CDLL, settings: Settings,
        img: np.ndarray, notes, frame: int):
    """
    Render the blocks.

    :param lib: C library for blocks.
    :param notes: MIDI notes.
    """
    lib.render_blocks(img, img.shape[1], img.shape[0],
            0, np.array([1], dtype=np.int32), np.array([1], dtype=np.int32))
