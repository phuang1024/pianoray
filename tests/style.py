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
import pathlib

MAX_LEN = 80   # Max line length.

RESET = "\x1b[39m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"

# List of (dir, recursive, (glob1, glob2, ...))
PATHS = (
    (".",         False, ("*.md", "*.gitignore", "*.txt")),
    ("./build",   False, ("*.py",)),
    ("./docs",    True,  ("*.rst", "*.py", "Makefile")),
    ("./src",     True,  ("*.py", "*.java", "Makefile")),
    ("./tests",   True,  ("*.py",)),
)


def print_msg(ok: bool, path, msg):
    sys.stdout.write(GREEN if ok else RED)
    print(str(path)+":", msg)


def test_file(path):
    exitcode = 0

    with open(path, "r") as file:
        data = file.read()

    if not data.endswith("\n"):
        print_msg(False, path, "no blank line at the end")
        exitcode = 1

    for i, line in enumerate(data.split("\n")):
        if line.endswith(" "):
            print_msg(False, path, f"line {i+1}: trailing whitespace")
            exitcode = 1
        if len(line) > MAX_LEN:
            print_msg(False, path, f"line {i+1}: longer than {MAX_LEN} chars")
            exitcode = 1

    if exitcode == 0:
        print_msg(True, path, "OK")
    return exitcode


def test_dir(directory, rec, globs):
    exitcode = 0

    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        abspath = os.path.realpath(path)

        if rec and os.path.isdir(abspath):
            exitcode = max(exitcode, test_dir(path, rec, globs))

    path = pathlib.Path(directory)
    for glob in globs:
        for relpath in path.glob(glob):
            abspath = os.path.realpath(relpath)
            if os.path.isfile(abspath):
                exitcode = max(exitcode, test_file(relpath))

    return exitcode


def main():
    exitcode = 0
    for path in PATHS:
        exitcode = max(exitcode, test_dir(*path))
    sys.stdout.write(RESET)
    sys.stdout.flush()
    return exitcode


if __name__ == "__main__":
    sys.exit(main())
