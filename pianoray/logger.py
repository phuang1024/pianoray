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
import termcolor
from datetime import datetime


def time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def log(type: str, msg: str, color: str):
    s = f"[{time()}] {type}:"
    s += " " * (6-len(type))
    s += msg
    print(termcolor.colored(s, color), file=sys.stderr)

def info(msg: str) -> None:
    """
    Info log to stderr.
    Color: blue
    """
    log("INFO", msg, "blue")

def warn(msg: str) -> None:
    """
    Warning log to stderr.
    Color: yellow
    """
    log("WARN", msg, "yellow")

def error(msg: str) -> None:
    """
    Error log to stderr.
    Color: red
    """
    log("ERROR", msg, "red")
