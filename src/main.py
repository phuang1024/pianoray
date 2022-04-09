#
#  PianoRay
#  Piano performance visualizer.
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

import argparse
import json
import sys

from . import logger
from .settings import Settings
from .utils import VERSION


def main():
    parser = argparse.ArgumentParser(
        description="Piano performance visualizer.")
    parser.add_argument("-V", "--version",
        help="Show version info.", action="store_true")
    parser.add_argument("-s", "--settings",
        help="Path to settings JSON file.")
    parser.add_argument("-o", "--output",
        help="Output video file.")
    parser.add_argument("-c", "--cache",
        help="Cache path (default .prcache)", default=".prcache")
    args = parser.parse_args()

    if args.version:
        print(f"Pianoray v{VERSION}")
        return 0

    if args.settings is None:
        logger.error("Please provide an argument for settings.")
        return 1
    if args.output is None:
        logger.error("Please provide an argument for output.")
        return 1

    with open(args.settings, "r") as fp:
        settings = Settings(json.load(fp))

    return 0


if __name__ == "__main__":
    sys.exit(main())
