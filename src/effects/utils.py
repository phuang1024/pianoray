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

from typing import Tuple

import numpy as np

from ..settings import Settings


def bounds(v, vmin, vmax):
    """
    Bound v between vmin and vmax.
    """
    return min(max(v, vmin), vmax)


def is_white_key(key: int) -> bool:
    """
    If the key is a white key on piano.
    """
    return (key % 12) not in (1, 4, 6, 9, 11)

def key_pos(key: int) -> float:
    """
    Position of the center of the key on the keyboard.
    Factor from 0 to 1 (start of first key to end of last).
    """
    white_width = 1 / 52

    last_white = False  # Last key was white
    pos = 0
    for k in range(key+1):
        white = is_white_key(k)
        if white:
            if last_white:
                pos += white_width
            else:
                pos += white_width / 2
        else:
            pos += white_width / 2
        last_white = white

    return pos

def key_coords(settings: Settings, key: int) -> Tuple[float, float]:
    """
    Horizontal (x) coordinates of key on the screen.

    :param key: Key.
    :return: ``(start_coord, end_coord)`` of key.
    """
    center = np.interp(key_pos(key), (0, 1), (0, settings.video.resolution[0]))
    white_width = settings.video.resolution[0] / 52
    black_width = white_width * settings.piano.black_width_fac
    width = white_width if is_white_key(key) else black_width
    half = width / 2
    return (center-half, center+half)


def note_coords(settings: Settings, event_frame: float,
        frame: float) -> float:
    """
    Vertical (y) coordinates of an event as it is dropping from the top
    to the keyboard.

    :param event_frame: The time of the event.
    :param frame: Current frame.
    :return: Y pixel position.
    """
    height = settings.video.resolution[1] / 2
    speed = (settings.blocks.speed * height / settings.video.fps)
    delta = speed * (frame-event_frame)
    return height + delta
