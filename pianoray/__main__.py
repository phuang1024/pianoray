"""
Main entry point.
"""

import argparse
import json
import os
import sys
from ast import literal_eval
from pathlib import Path

from . import logger
from .settings import Settings
from .utils import SETTINGS_DEFAULT, VERSION

from .render import render_video
from .view import view_video


def render(args):
    """
    Call this when the user requests render, e.g.
    pianoray render ...
    """
    if args.output.exists() and not args.yes:
        if input(f"Overwrite output file {args.output}? [y/N] ") \
                .lower().strip() != "y":
            return 3

    with open(args.settings, "r") as fp:
        settings = Settings(json.load(fp))
    default = Settings(SETTINGS_DEFAULT)
    settings._merge(default)

    render_video(args, settings, args.output, args.cache)

    if args.preview:
        logger.info("Opening output with xdg-open")
        os.system(f"xdg-open {args.output}")


def view(args):
    """
    Called when the user requests view e.g.
    pianoray view ...
    """
    view_video(args.file)


def main():
    """
    Main entry point.
    """
    version_str = f"Pianoray v{VERSION}"

    parser = argparse.ArgumentParser(
        description="Piano performance visualizer.")
    subparsers = parser.add_subparsers(title="subcommands", dest="subparser")
    parser.add_argument("-V", "--version", action="version",
        help="Show version info.", version=version_str)
    parser.add_argument("-y", "--yes",
        help="Don't prompt overwrite.", action="store_true")

    render_parser = subparsers.add_parser("render",
        help="Render a video.")
    render_parser.add_argument("-s", "--settings", required=True,
        help="Path to settings JSON file.", type=Path)
    render_parser.add_argument("-o", "--output", required=True,
        help="Output video file.", type=Path)
    render_parser.add_argument("-c", "--cache", default=".prcache",
        help="Cache path (default .prcache)", type=Path)
    render_parser.add_argument("-p", "--preview", action="store_true",
        help="Open output file after rendering")
    render_parser.add_argument("-r", "--resume", type=literal_eval,
        help="Whether to resume previous render (omit for prompt).")

    view_parser = subparsers.add_parser("view",
        help="View a video file in a GUI video.")
    view_parser.add_argument("file", help="Path to file to view.")

    args = parser.parse_args()
    logger.info(version_str)

    if args.subparser == "render":
        render(args)
    elif args.subparser == "view":
        view(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())
