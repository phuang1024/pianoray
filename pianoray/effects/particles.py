"""
Particles.
"""

import os

import numpy as np

from ..cpp import Types
from ..utils import strnum
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

        cache_in = self.cache / "ptcls" / strnum(frame-1)
        cache_out = self.cache / "ptcls" / strnum(frame)
        if not cache_in.is_file():
            cache_in = ""

        props_args = [props.video.fps, props.ptcls.pps, props.ptcls.air_resist,
            props.ptcls.lifetime, props.ptcls.x_vel, props.ptcls.y_vel,
            props.ptcls.wind_strength, props.ptcls.heat_strength, props.ptcls.gravity]

        self.libs["ptcls"].render_ptcls(
            img, img.shape[1], img.shape[0],
            frame,
            Types.cpath(cache_in), Types.cpath(cache_out),
            len(notes), keys, starts, ends,
            *props_args,
        )
