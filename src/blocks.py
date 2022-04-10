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

import numpy as np

from .pianoutils import key_coords, note_coords
from .settings import Settings


def render_blocks(settings: Settings, img: np.ndarray, notes,
        frame: int) -> None:
    """
    Render blocks.

    :param settings: Settings.
    :param img: Image.
    :param notes: MIDI notes.
    :param frame: Current frame.
    """
    for note, vel, start, end in notes:
        start_y = note_coords(settings, start, frame)
        end_y = note_coords(settings, end, frame)
        start_x, end_x = key_coords(settings, note)

        start_x, end_x, start_y, end_y = map(int,
            (start_x, end_x, start_y, end_y))

        img[start_y:end_y, start_x:end_x, ...] = 255
