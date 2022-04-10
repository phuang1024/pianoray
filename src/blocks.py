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

from math import hypot

import numpy as np

from .pianoutils import key_coords, note_coords
from .settings import Settings
from .utils import bounds


def dist_to_block(px, py, x, y, w, h, r) -> float:
    """
    Distance to a block.

    :param px, py: Point coordinates.
    :param x, y, w, h: Coordinates of block.
    :param r: Radius of block corners.
    """
    half_x = x + w/2
    half_y = y + h/2
    if px > half_x:
        px -= 2 * (px-x)
    if py > half_y:
        py -= 2 * (py-y)

    cx = x + r
    cy = y + r

    if px < cx and py < cy:
        return hypot(cx-px, cy-py) - r
    elif px < x and py >= cy:
        return px - x
    elif px >= cx and py < y:
        return py - y
    else:
        return 0


def render_blocks(settings: Settings, img: np.ndarray, notes,
        frame: int) -> None:
    """
    Render blocks.

    :param settings: Settings.
    :param img: Image.
    :param notes: MIDI notes.
    :param frame: Current frame.
    """
    width, height = settings.resolution

    for note, vel, start, end in notes:
        start_y = note_coords(settings, start, frame)
        end_y = note_coords(settings, end, frame)
        if start_y < 0 or end_y > height/2:
            continue

        start_y = bounds(start_y, 0, height/2)
        end_y = bounds(end_y, 0, height/2)
        start_x, end_x = key_coords(settings, note)

        x = start_x
        y = end_y
        w = end_x - start_x
        h = start_y - end_y
        x, y, w, h = map(int, (x, y, w, h))

        for py in range(bounds(x-2, 0, height-1), bounds(x+w+3, 0, height-1)):
            for px in range(bounds(y-2, 0, width-1), bounds(y+h+3, 0, width-1)):
                dist = dist_to_block(px, py, x, y, w, h, 5)

                color = np.interp(dist, (1, 0), (0, 255))
                color = bounds(color, 0, 255)
                img[py, px, :] = color
