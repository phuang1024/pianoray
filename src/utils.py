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

import os
import shutil

VERSION = "0.0.1"

PARENT = os.path.dirname(os.path.abspath(__file__))

FFMPEG = shutil.which("ffmpeg")
GCC = shutil.which("g++")
assert FFMPEG is not None
assert GCC is not None


SETTINGS_DEFAULT = {
    "video": {
        "fps": 30,
        "resolution": (1920, 1080),
        "vcodec": "libx265",
        "duration": None,
    },
    "audio": {
        "path": None,
        "start": 0,
    },
    "composition": {
        "margin_start": 2,
        "margin_end": 2,
    },
    "piano": {
        "black_width_fac": 0.6,
    },
    "blocks": {
        "speed": 0.5,
        "color": [185, 200, 255],
        "radius": 0.25,
    },
    "midi": {
        "file": None,
        "speed": 1,
    },
}


def forever():
    """
    Generator for indefinite tqdm progressbar.
    """
    while True:
        yield
