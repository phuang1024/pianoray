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

import sys
import os
import shutil
import json
import termcolor
from subprocess import Popen, PIPE
from typing import Any, Sequence, Union
from . import logger
from .utils import readall

PYTHON = shutil.which("python3")
JAVA = shutil.which("java")


class KernelException(Exception):
    """
    An error occured.
    """


class Kernel:
    """
    Represents one kernel.

    Every kernel is a directory (folder) of files. Detects if it is Python, Java,
    Executable, etc. The main entry point is ``main.*``, case independent. If
    there is more than one such entry point, an arbitrary one will be chosen.

    Use the ``__call__`` method to communicate JSON.
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
        files = filter(lambda s: s.lower().startswith("main"),
            os.listdir(path))
        try:
            entry = next(files)
        except StopIteration:
            raise KernelException(f"{self} directory has no main file.")
        ext = entry.split(".")[-1]

        if ext == "py":
            self.lang = "PYTHON"
            if not PYTHON:
                raise KernelException(f"{self} python3 not found.")
        elif ext == "class":
            self.lang = "JAVA"
            if not JAVA:
                raise KernelException(f"{self} java not found.")
        elif ext == "out":
            self.lang = "EXEC"
        else:
            raise KernelException(f"{self} invalid file ending: {entry}")

        self.dir_path = path
        self.exe_path = os.path.join(path, entry)
        self.name = os.path.basename(self.dir_path)

    def __repr__(self) -> str:
        return f"<class pianoray.Kernel(name={self.name})>"

    def __call__(self, obj: Any, async_: bool = False,
            args: Sequence[str] = ()) -> Union[Any, "KernelRun"]:
        """
        Call with json input and output.

        :param obj: Input JSON object.
        :param async_: Whether to run asynchronously.
            if True, return KernelRun.
            else, return JSON output.
        :param args: CLI arguments.
        """
        run = KernelRun(self, obj, args)
        if async_:
            return run
        else:
            run.wait()
            return run.output

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
        proc = Popen(pre_args, stdin=PIPE, stdout=PIPE, stderr=PIPE,
            cwd=self.dir_path)
        return proc


class KernelRun:
    """
    Used to manage a running kernel with json io.
    Useful for async kernel execution.
    """

    kernel: Kernel
    proc: Popen

    _output: Any  # Output object.
    _read_output: bool  # Whether output was read.

    def __init__(self, kernel: Kernel, stdin: Any,
            args: Sequence[str] = ()) -> None:
        """
        Initialize run.

        :param kernel: Kernel instance.
        :param stdin: Input JSON object.
        :param args: CLI arguments.
        """
        proc = kernel.proc(args)
        proc.stdin.write(json.dumps(stdin).encode())
        proc.stdin.write(b"\n")
        proc.stdin.flush()
        proc.stdin.close()

        self.kernel = kernel
        self.proc = proc
        self._output = None
        self._read_output = False

    def __repr__(self) -> str:
        return f"<class pianoray.KernelRun(name={self.kernel.name})>"

    @property
    def alive(self):
        """
        If the process is still running.
        """
        return self.proc.poll() is not None

    def wait(self):
        """
        Wait for the process to finish.
        """
        self.proc.wait()

    @property
    def output(self):
        """
        Get process output as JSON object.
        If process is alive, raises KernelException.
        """
        if self.proc.poll() is None:
            raise KernelException(f"{self} cannot read output while process "
                "is still running.")
        if (ret := self.proc.returncode) != 0:
            logger.error(f"{self} exit code is {ret}.")

            choice = input("Show stderr text of kernel? [Y/n] ").strip().lower()
            if choice != "n":
                err = readall(self.proc.stderr).decode()
                print(termcolor.colored(err, "white", attrs={"dark"}), end="")

            raise KernelException(f"{self} exit code is {ret}.")

        if not self._read_output:
            self._output = json.loads(readall(self.proc.stdout))
            self._read_output = True
        return self._output
