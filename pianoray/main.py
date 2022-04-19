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
import os
import sys

from . import logger
from .settings import Settings
from .utils import SETTINGS_DEFAULT, VERSION

from .render import render_video
from .view import view_video


def render(args):
    if args.settings is None:
        logger.error("Please provide an argument for settings.")
        return 1
    if args.output is None:
        logger.error("Please provide an argument for output.")
        return 1

    if os.path.isfile(args.output) and not args.yes:
        print(f"Output file {args.output} already exists.")
        if input("Overwrite file? [y/N] ").lower().strip() != "y":
            return 3

    with open(args.settings, "r") as fp:
        settings = Settings(json.load(fp))
    default = Settings(SETTINGS_DEFAULT)
    settings._merge(default)

    render_video(settings, args.output, args.cache)

    if args.preview:
        os.system(f"xdg-open {args.output}")


def view(args):
    if len(args.options) == 0:
        logger.error("Please provide the video file to view.")
        return 1

    view_video(args.options[0])


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
    parser.add_argument("-p", "--preview",
        help="Open output file after rendering", action="store_true")
    parser.add_argument("-y", "--yes",
        help="Don't prompt overwrite.", action="store_true")
    parser.add_argument("mode", choices={"render", "view"}, nargs="?",
        help="Mode to run.")
    parser.add_argument("options", nargs="*",
        help="Any other positional arguments.")
    args = parser.parse_args()

    if args.version:
        print(f"Pianoray v{VERSION}")
        return 0

    if args.mode is None or args.mode == "render":
        return render(args)
    elif args.mode == "view":
        return view(args)


if __name__ == "__main__":
    sys.exit(main())
