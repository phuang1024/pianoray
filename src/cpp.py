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


def build_lib(files: Sequence[str], cache: str, name: str) -> ctypes.CDLL:
    """
    Initialize the lib.

    :param files: C files.
    :param cache: Cache directory.
    :param name: Name of the library.
    :return: C library.
    """
    cache = os.path.join(cache, name)
    os.makedirs(self.cache, exist_ok=True)

    obj_files = []
    for f in files:
        name = os.path.basename(f)
        obj_name = os.path.splitext(name)[0] + ".o"
        obj_path = os.path.join(self.cache, obj_name)
        obj_files.append(obj_path)
        _compile(f, obj_path)

    lib_path = os.path.join(self.cache, f"lib{name}.so")
    _link(obj_files, lib_path)

    return ctypes.CDLL(lib_path)

def _compile(cpp, obj):
    args = [GCC, "-Wall", "-O3", "-c", "-fPIC", cpp, "-o", obj]
    Popen(args).wait()

def _link(obj_files, lib_path):
    args = [GCC, "-shared", "-o", lib_path, *obj_files]
    Popen(args).wait()
