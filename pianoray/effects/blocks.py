"""
Blocks effect.
"""

import numpy as np

from ..cpp import Types
from .effect import Effect


class Blocks(Effect):
    """
    The blocks that fall down.
    """

    def render(self, props, img: np.ndarray, frame: int, notes):
        """
        Render the blocks.
        :param notes: MIDI notes from parse_midi.
        """
        keys = np.array([n.note for n in notes], dtype=Types.int)
        starts = np.array([n.start for n in notes], dtype=Types.double)
        ends = np.array([n.end for n in notes], dtype=Types.double)

        props_args = [props.video.fps, props.blocks.speed,
            props.piano.black_width_fac, props.blocks.radius,
            np.array(props.blocks.color, dtype=np.uint8),
            props.blocks.glow_intensity, props.blocks.glow_radius,
            np.array(props.blocks.glow_color, dtype=np.uint8),
        ]

        self.libs["blocks"].render_blocks(
            img, img.shape[1], img.shape[0],
            frame,
            len(notes), keys, starts, ends,
            *props_args,
        )
