"""
Handles loading libraries.
Calls functions from ../cpp.py
"""

import ctypes
import os
from pathlib import Path
from typing import Mapping

from ..cpp import build_lib, Types


def load_libs(cache: Path) -> Mapping[str, ctypes.CDLL]:
    """
    Load C libraries. Also sets the argtypes and restypes.
    """
    cache = cache / "c_libs"
    cache.mkdir(parents=True, exist_ok=True)

    blocks = build_lib(
        ["cutils/blocks.cpp"],
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
        ["cutils/glare.cpp"],
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

    keyboard = build_lib(
        ["cutils/keyboard.cpp"],
        cache,
        "keyboard",
    )
    keyboard.render_octave_lines.argtypes = [
        Types.img, Types.int, Types.int,
    ]

    particles = build_lib(
        ["cutils/particles.cpp"],
        cache,
        "particles",
    )
    particles.render_ptcls.argtypes = [
        Types.img, Types.int, Types.int,
        Types.int,
        Types.path, Types.path,
        Types.int, Types.arr_int, Types.arr_double, Types.arr_double,
        Types.int, Types.double, Types.double, Types.double, Types.double, Types.double,
            Types.double, Types.double, Types.double,
    ]

    return {
        "blocks": blocks,
        "glare": glare,
        "keyboard": keyboard,
        "ptcls": particles,
    }
