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


def info(msg: str) -> None:
    """
    Info log to stderr.
    Color: blue
    """
    print(termcolor.colored("INFO:  "+msg, "blue"), file=sys.stderr)

def warn(msg: str) -> None:
    """
    Warning log to stderr.
    Color: yellow
    """
    print(termcolor.colored("WARN:  "+msg, "yellow"), file=sys.stderr)

def error(msg: str) -> None:
    """
    Error log to stderr.
    Color: red
    """
    print(termcolor.colored("ERROR: "+msg, "red"), file=sys.stderr)
