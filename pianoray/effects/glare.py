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

import os
import random

import numpy as np

from ..cpp import Types
from .effect import Effect


class Glare(Effect):
    """
    Light glare when notes play.
    """

    def __init__(self, settings, cache, libs, notes) -> None:
        super().__init__(settings, cache, libs)

        for note in notes:
            streaks = []
            for _ in range(settings.glare.streaks):
                angle = random.randint(0, 255)
                streaks.append(angle)
            note.attrs["glare.streak_angles"] = streaks

    def render(self, settings, img: np.ndarray, frame: int, notes):
        """
        Render the glare.

        :param notes: MIDI notes from parse_midi.
        """
        keys = np.array([n.note for n in notes], dtype=Types.int)
        starts = np.array([n.start for n in notes], dtype=Types.double)
        ends = np.array([n.end for n in notes], dtype=Types.double)

        angles = []
        for note in notes:
            angles.extend(note.attrs["glare.streak_angles"])
        angles = np.array(angles, dtype=np.uint8)

        settings = self.settings
        settings_args = [settings.piano.black_width_fac,
            settings.glare.radius, settings.glare.intensity,
            settings.glare.jitter, settings.glare.streaks]

        self.libs["glare"].render_glare(
            img, img.shape[1], img.shape[0],
            frame,
            len(notes), keys, starts, ends, angles,
            *settings_args,
        )
