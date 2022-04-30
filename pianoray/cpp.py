import ctypes
import os
from pathlib import Path
from subprocess import Popen
from typing import Sequence

import numpy as np
from numpy.ctypeslib import ndpointer

from . import logger
from .utils import GCC

ROOT = Path(__file__).absolute().parent

CPP_UTILS = ROOT / "cutils"
CPP_UTILS_FILES = [CPP_UTILS / f
    for f in CPP_UTILS.iterdir() if f.suffix == ".cpp"]


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
    path = ndpointer(dtype=char, ndim=1, flags=_arr_flags)

    @staticmethod
    def cpath(path: str):
        """
        Return C path (numpy array of chars, null terminated).
        """
        data = [c for c in path.encode()]
        data.append(0)
        return np.array(data, dtype=np.int8)


def build_lib(files: Sequence[str], cache: Path, name: str) -> ctypes.CDLL:
    """
    Initialize the lib.

    :param files: C files relative to THIS file.
    :param cache: Cache directory.
    :param name: Name of the library.
    :return: C library.
    """
    logger.info(f"Building C library {name}")

    cache = cache / name
    os.makedirs(cache, exist_ok=True)

    files = [ROOT/f for f in files]
    files.extend(CPP_UTILS_FILES)

    obj_files = []
    for f in files:
        obj_path = str(f.with_suffix(".o"))
        obj_files.append(obj_path)
        compile(str(f), obj_path)

    lib_path = str(cache / f"lib{name}.so")
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
