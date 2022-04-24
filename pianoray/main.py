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
    """
    if args.settings is None:
        logger.error("Please provide an argument for settings.")
        return 1
    if args.output is None:
        logger.error("Please provide an argument for output.")
        return 1
        """

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
        logger.info("Opening output with xdg-open")
        os.system(f"xdg-open {args.output}")


def view(args):
    view_video(args.file)


def main():
    parser = argparse.ArgumentParser(
        description="Piano performance visualizer.")
    subparsers = parser.add_subparsers(title="subcommands", dest="subparser")
    parser.add_argument("-V", "--version", action="version",
        help="Show version info.", version=f"Pianoray v{VERSION}")
    parser.add_argument("-y", "--yes",
        help="Don't prompt overwrite.", action="store_true")

    render_parser = subparsers.add_parser("render",
        help="Render a video.")
    render_parser.add_argument("-s", "--settings", required=True,
        help="Path to settings JSON file.")
    render_parser.add_argument("-o", "--output", required=True,
        help="Output video file.")
    render_parser.add_argument("-c", "--cache", default=".prcache",
        help="Cache path (default .prcache)")
    render_parser.add_argument("-p", "--preview", action="store_true",
        help="Open output file after rendering")

    view_parser = subparsers.add_parser("view",
        help="View a video file in a GUI video.")
    view_parser.add_argument("file", help="Path to file to view.")

    args = parser.parse_args()
    if args.subparser == "render":
        render(args)
    elif args.subparser == "view":
        view(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())
