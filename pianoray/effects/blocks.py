import numpy as np

from ..cpp import Types
from .effect import Effect


class Blocks(Effect):
    """
    The blocks that fall down.
    """

    def render(self, settings, img: np.ndarray, frame: int, notes):
        """
        Render the blocks.
        :param notes: MIDI notes from parse_midi.
        """
        keys = np.array([n.note for n in notes], dtype=Types.int)
        starts = np.array([n.start for n in notes], dtype=Types.double)
        ends = np.array([n.end for n in notes], dtype=Types.double)

        settings = self.settings
        settings_args = [settings.video.fps, settings.blocks.speed,
            settings.piano.black_width_fac, settings.blocks.radius,
            np.array(settings.blocks.color, dtype=np.uint8),
            settings.blocks.glow_intensity, settings.blocks.glow_radius,
            np.array(settings.blocks.glow_color, dtype=np.uint8),
        ]

        self.libs["blocks"].render_blocks(
            img, img.shape[1], img.shape[0],
            frame,
            len(notes), keys, starts, ends,
            *settings_args,
        )
