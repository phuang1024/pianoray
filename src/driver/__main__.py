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
import argparse
from .kernel import Kernel, KernelException
from .pipeline import BasePipeline
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


def execute_graph(path, output, kernels):
    if not path.count(":") == 1:
        logger.error("Pipeline path must be \"/path/file.py:PipelineClass\"")
        return

    path, cls_name = path.split(":")
    parent = os.path.dirname(path)
    mod_name = os.path.basename(path)[:-3]

    sys.path.insert(0, parent)
    mod = __import__(mod_name)
    cls = getattr(mod, cls_name)
    sys.path.pop(0)

    if not issubclass(cls, BasePipeline):
        logger.error(f"Class {cls} needs to extend from pianoray.BasePipeline")
        return

    graph = cls(kernels)
    graph.render(output)


def main():
    parser = argparse.ArgumentParser(
        description="Video rendering pipeline with piano visualization. "
                    "This program drives the rendering kernels.")
    parser.add_argument("-V", "--version", help="Print version.", action="store_true")
    parser.add_argument("-p", "--paths", help="Path to kernel executables (sep=\":\").",
        required=True)
    parser.add_argument("-o", "--output", help="Output video file.", required=True)
    parser.add_argument("graph", help="File containing pipeline e.g. file.py:PipelineClass")
    args = parser.parse_args()

    if args.version:
        print("PianoRay Driver 0.0.1")
        return

    kernels = load_kernels(args.paths.split(os.path.pathsep))
    execute_graph(os.path.realpath(args.graph), args.output, kernels)


if __name__ == "__main__":
    main()
