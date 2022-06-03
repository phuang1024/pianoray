"""
C++ library compilation and handling.
"""

import ctypes
import os
import re
from pathlib import Path
from subprocess import Popen
from typing import Sequence

import numpy as np
from numpy.ctypeslib import ndpointer

#from . import logger
#from .utils import GCC

ROOT = Path(__file__).absolute().parent

CPP_UTILS = ROOT / "cutils"


class Types:
    """
    C++ types. Assign a sequence of types to func.argtypes:

    lib.render_thing.argtypes = [img, int, int, float, double, ...]
    """
    _arr_flags = "aligned, c_contiguous"

    char = ctypes.c_int8
    uchar = ctypes.c_uint8
    int = ctypes.c_int32
    uint = ctypes.c_uint32
    float = ctypes.c_float
    double = ctypes.c_double

    _arr_code = "arr_{0} = ndpointer(dtype={0}, ndim=1, flags=_arr_flags)"
    for t in ("char", "uchar", "int", "uint", "float", "double"):
        exec(_arr_code.format(t))

    @staticmethod
    def cpath(path):
        """
        Return C path (numpy array of chars, null terminated).
        """
        data = [c for c in str(path).encode()]
        data.append(0)
        return np.array(data, dtype=np.int8)

    @staticmethod
    def c_to_attr(type):
        """
        Convert C type string to this class's attribute name.
        e.g. "unsigned int" to "uint"
        """
        if type in ("char", "int", "float", "double"):
            return type
        elif type.startswith("unsigned"):
            return "u" + type.split(" ")[1]
        else:
            raise ValueError(f"Cannot understand C type {type}")


def build_lib(files: Sequence[str], cache: Path, name: str) -> ctypes.CDLL:
    """
    Build and load a library.

    :param files: C files relative to THIS file.
    :param cache: Cache directory.
    :param name: Name of the library.
    :return: C library.
    """
    logger.info(f"Building C library {name}")

    cache = cache / name
    os.makedirs(cache, exist_ok=True)

    files = [ROOT/f for f in files]

    obj_files = []
    for f in files:
        obj_path = str(cache / f.with_suffix(".o").name)
        obj_files.append(obj_path)
        compile(str(f), obj_path)

    lib_path = str(cache / f"lib{name}.so")
    link(obj_files, lib_path)

    return ctypes.CDLL(lib_path)

def compile(cpp, obj):
    """
    Compile a C++ file and output to obj file.
    """
    args = [GCC, "-Wall", "-O3", "-c", "-fPIC", cpp, "-o", obj, "-I", CPP_UTILS]
    p = Popen(args)
    p.wait()
    assert p.returncode == 0

def link(obj_files, lib_path):
    """
    Link object files.
    """
    args = [GCC, "-shared", "-o", lib_path, *obj_files]
    p = Popen(args)
    p.wait()
    assert p.returncode == 0


def parse_args(path, func_name):
    """
    Use regex to parse the arguments of a C++ function.
    Don't need to manually set them with CDLL.argtypes = [...]
    """
    with open(path, "r") as fp:
        data = fp.read()

    start = re.search(r'extern\s*"C"\s*void\s*' + func_name, data)
    if start is None:
        raise ValueError("Function declaration not found.")
    start = start.start()

    arg_str = data[data.find("(", start)+1 : data.find(")", start)]
    arg_strs = map(str.strip, arg_str.strip().split(","))
    args = []
    for s in arg_strs:
        type, name = s.rsplit(" ", 1)
        ptr = "*" in type
        type = type.replace("*", "").replace(" ", "").strip()

        attr = Types.c_to_attr(type)
        if ptr:
            attr = "arr_" + attr

        args.append(getattr(Types, attr))

    return args
