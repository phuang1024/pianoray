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
                except KernelException:
                    logger.warn(f"Failed to load kernel: {dir}")

                if dir in kernels:
                    logger.warn(f"Duplicate kernel: {dir}, not loaded.")
                else:
                    kernels[dir] = k
                    logger.info(f"Loaded kernel: {dir}")

    return kernels


def execute_graph(path, output, kernels):
    if not path.count(":") == 1:
        logger.error("Pipeline path must be \"/path/file.py:PipelineClass\"")
        return 1

    path, cls_name = path.split(":")
    parent = os.path.dirname(path)
    mod_name = os.path.basename(path)[:-3]

    sys.path.insert(0, parent)
    mod = __import__(mod_name)
    if not hasattr(mod, cls_name):
        logger.error(f"Class {cls_name} not found.")
        return 1
    cls = getattr(mod, cls_name)
    sys.path.pop(0)

    if not issubclass(cls, BasePipeline):
        logger.error(f"Class {cls} needs to extend from pianoray.BasePipeline")
        return 1

    graph = cls(kernels)
    graph.render(output)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Video rendering pipeline with piano visualization.")
    parser.add_argument("-V", "--version", help="Version.", action="store_true")
    parser.add_argument("-p", "--paths", help="Directories to search for "
        "kernels. (sep=\":\").", required=True)
    parser.add_argument("-o", "--output", help="Output video file.",
        required=True)
    parser.add_argument("graph", help="Pipeline file and class name e.g. "
        "file.py:PipelineClass")
    args = parser.parse_args()

    if args.version:
        print("PianoRay Driver 0.0.1")
        return

    kernels = load_kernels(args.paths.split(os.path.pathsep))
    ret = execute_graph(os.path.realpath(args.graph), args.output, kernels)
    sys.exit(ret)


if __name__ == "__main__":
    main()
