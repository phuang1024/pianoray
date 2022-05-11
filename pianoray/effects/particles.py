"""
Particles.
"""

import numpy as np

from ..cpp import Types
from .effect import Effect


class Particles(Effect):
    """
    Particles emit from keys.
    """

    def render(self, props, img: np.ndarray, frame: int, notes):
        """
        Render particles.

        :param notes: MIDI notes.
        """
        keys = np.array([n.note for n in notes], dtype=Types.int)
        starts = np.array([n.start for n in notes], dtype=Types.double)
        ends = np.array([n.end for n in notes], dtype=Types.double)

        props_args = [
        ]

        self.libs["ptcls"].render_ptcls(
            img, img.shape[1], img.shape[0],
            frame,
            len(notes), keys, starts, ends,
        )
