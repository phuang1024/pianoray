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
