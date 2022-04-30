#
#  PianoRay
#  Piano performance visualizer.
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
from pathlib import Path
from typing import Mapping

from ..cpp import build_lib, Types


def load_libs(cache: Path) -> Mapping[str, ctypes.CDLL]:
    """
    Load C libraries.
    """
    cache = cache / "c_libs"
    os.makedirs(cache, exist_ok=True)

    blocks = build_lib(
        ["effects/blocks.cpp"],
        cache,
        "blocks",
    )
    blocks.render_blocks.argtypes = [
        Types.img, Types.int, Types.int,
        Types.int,
        Types.int, Types.arr_int, Types.arr_double, Types.arr_double,
        Types.int, Types.double, Types.double, Types.double, Types.arr_uchar,
            Types.double, Types.double, Types.arr_uchar,
    ]

    glare = build_lib(
        ["effects/glare.cpp"],
        cache,
        "glare",
    )
    glare.render_glare.argtypes = [
        Types.img, Types.int, Types.int,
        Types.int,
        Types.int, Types.arr_int, Types.arr_double, Types.arr_double,
            Types.arr_uchar,
        Types.double, Types.double, Types.double, Types.double, Types.int,
    ]

    return {
        "blocks": blocks,
        "glare": glare,
    }
