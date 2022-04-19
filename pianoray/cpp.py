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
from subprocess import Popen
from typing import Sequence

import numpy as np
from numpy.ctypeslib import ndpointer

from . import logger
from .utils import GCC

PARENT = os.path.dirname(os.path.abspath(__file__))

CPP_UTILS = os.path.join(PARENT, "cutils")
CPP_UTILS_FILES = [os.path.join(CPP_UTILS, f)
    for f in os.listdir(CPP_UTILS) if f.endswith(".cpp")]


class Types:
    _arr_flags = "aligned, c_contiguous"

    char = ctypes.c_int8
    uchar = ctypes.c_uint8
    int = ctypes.c_int32
    uint = ctypes.c_uint32
    float = ctypes.c_float
    double = ctypes.c_double

    arr_uchar = ndpointer(dtype=uchar, ndim=1, flags=_arr_flags)
    arr_int = ndpointer(dtype=int, ndim=1, flags=_arr_flags)
    arr_double = ndpointer(dtype=double, ndim=1, flags=_arr_flags)

    img = ndpointer(dtype=uchar, ndim=3, flags=_arr_flags)


def build_lib(files: Sequence[str], cache: str, name: str) -> ctypes.CDLL:
    """
    Initialize the lib.

    :param files: C files relative to THIS file.
    :param cache: Cache directory.
    :param name: Name of the library.
    :return: C library.
    """
    logger.info(f"Building C library {name}")

    cache = os.path.join(cache, name)
    os.makedirs(cache, exist_ok=True)

    files = [os.path.join(PARENT, f) for f in files]
    files.extend(CPP_UTILS_FILES)

    obj_files = []
    for f in files:
        fname = os.path.basename(f)
        obj_name = os.path.splitext(fname)[0] + ".o"
        obj_path = os.path.join(cache, obj_name)
        obj_files.append(obj_path)
        compile(f, obj_path)

    lib_path = os.path.join(cache, f"lib{name}.so")
    link(obj_files, lib_path)

    return ctypes.CDLL(lib_path)

def compile(cpp, obj):
    args = [GCC, "-Wall", "-O3", "-c", "-fPIC", cpp, "-o", obj, "-I", CPP_UTILS]
    p = Popen(args)
    p.wait()
    assert p.returncode == 0

def link(obj_files, lib_path):
    args = [GCC, "-shared", "-o", lib_path, *obj_files]
    p = Popen(args)
    p.wait()
    assert p.returncode == 0
