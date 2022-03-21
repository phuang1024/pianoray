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

import os
import shutil
import json
from subprocess import Popen, PIPE
from typing import Any, Sequence
from . import logger
from .utils import readall

PYTHON = shutil.which("python3")
JAVA = shutil.which("java")


class KernelException(Exception):
    """
    An error occured with ``pianoray.Kernel``.
    """


class Kernel:
    """
    Represents one kernel.
    Every kernel is a directory (folder) of files.
    Detects if it is Python, Java, Executable, etc.
    The main entry point is ``main.*``, case independent.
    If there is more than one such file, an arbitrary one will be chosen.
    """

    name: str

    dir_path: str
    """Path to directory"""

    exe_path: str
    """Path to entry point."""

    lang: str
    """PYTHON, JAVA, EXEC"""

    def __init__(self, path: str) -> None:
        """
        Initialize with path to directory.
        The directory must contain ``main.py``, ``main.class``, or ``main.out``,
        case insensitive.
        """
        path = os.path.realpath(path)
        files = filter(lambda s: s.lower().startswith("main"), os.listdir(path))
        try:
            entry = next(files)
        except StopIteration:
            raise KernelException("Kernel directory has no main file.")
        ext = entry.split(".")[-1]

        if ext == "py":
            self.lang = "PYTHON"
            if not PYTHON:
                raise KernelException("python3 not found.")
        elif ext == "class":
            self.lang = "JAVA"
            if not JAVA:
                raise KernelException("java not found.")
        elif ext == "out":
            self.lang = "EXEC"
        else:
            raise KernelException(f"Invalid file ending: {ext}")

        self.dir_path = path
        self.exe_path = os.path.join(path, entry)
        self.name = os.path.basename(self.dir_path)

    def proc(self, args: Sequence[str] = ()) -> Popen:
        """
        Open a process with all three streams PIPE.

        :param args: Extra arguments after ``exe_path``.
        """
        if self.lang == "PYTHON":
            pre_args = [PYTHON, self.exe_path]
        elif self.lang == "JAVA":
            pre_args = [JAVA, os.path.basename(self.exe_path)[:-6]]
        elif self.lang == "EXEC":
            pre_args = [self.exe_path]

        pre_args.extend(args)
        proc = Popen(pre_args, stdin=PIPE, stdout=PIPE, cwd=self.dir_path)
        return proc

    def run(self, stdin: bytes, args=()) -> bytes:
        """
        Run process with bytes input and output.
        """
        proc = self.proc(args)

        proc.stdin.write(stdin)
        proc.stdin.flush()
        proc.stdin.close()
        proc.wait()
        if proc.returncode != 0:
            logger.error(f"Kernel {self.name} exited with code {proc.returncode}")
            raise KernelException()

        data = readall(proc.stdout)
        return data

    def run_json(self, stdin: Any, args: Sequence[str] = ()) -> Any:
        """
        Run process with json input and output.
        Dump ``stdin`` as json into ``proc.stdin``.
        Return output as object parsed from ``proc.stdout``.
        """
        proc = self.proc(args)

        proc.stdin.write(json.dumps(stdin).encode())
        proc.stdin.write(b"\n")
        proc.stdin.flush()
        proc.stdin.close()
        proc.wait()
        if proc.returncode != 0:
            logger.error(f"Kernel {self.name} exited with code {proc.returncode}")
            raise KernelException()

        data = readall(proc.stdout)
        return json.loads(data)
