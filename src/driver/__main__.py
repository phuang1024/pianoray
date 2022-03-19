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
import argparse
from .kernel import Kernel, KernelException
from . import logger


def load_kernels(paths):
    kernels = {}
    for path in paths:
        for dir in os.listdir(path):
            p = os.path.join(path, dir)
            if os.path.isdir(p):
                try:
                    k = Kernel(p)
                    kernels[dir] = k
                    logger.info(f"Loaded kernel: {dir}")
                except (StopIteration, KernelException):
                    logger.warn(f"Failed to load kernel: {dir}")

    return kernels


def main():
    parser = argparse.ArgumentParser(
        description="Video rendering pipeline with piano visualization.\n"
                    "This program drives the rendering kernels.")
    parser.add_argument("-V", "--version", help="Print version.", action="store_true")
    parser.add_argument("-p", "--paths", help="Path to kernel executables (sep=\":\").",
        required=True)
    parser.add_argument("-v", "--verbose", help="Verbose output.", action="store_true")
    args = parser.parse_args()

    if args.version:
        print("PianoRay Driver 0.0.1")
        return

    logger.set_verbose(args.verbose)
    kernels = load_kernels(args.paths.split(os.path.pathsep))


if __name__ == "__main__":
    main()
