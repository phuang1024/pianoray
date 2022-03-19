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

    dir_path: str
    """Path to directory"""

    exe_path: str
    """Path to entry point."""

    lang: str
    """PYTHON, JAVA, EXEC"""

    def __init__(self, path):
        """
        Initialize with path to directory.
        """
        entry = next(filter(lambda s: s.lower().startswith("main"), os.listdir(path)))
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

    def run(self, args=()) -> Popen:
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
        proc = Popen(pre_args, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.dir_path)
        return proc

    def run_json(self, stdin, args=()):
        """
        Run process with json input and output.
        Dump ``stdin`` as json into ``proc.stdin``.
        Return output as parsed json.
        """
        proc = self.run(args)

        proc.stdin.write(json.dumps(stdin).encode())
        proc.stdin.write(b"\n")
        proc.stdin.flush()
        proc.stdin.close()
        proc.wait()

        return json.loads(readall(proc.stdout))
