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

import numpy as np
from tqdm import trange

from . import logger
from .blocks import render_blocks
from .midi import parse_midi
from .settings import Settings
from .video import Video


def render_video(settings: Settings, out: str, cache: str) -> None:
    os.makedirs(cache, exist_ok=True)

    notes = parse_midi(settings)
    duration = int(max(x[3] for x in notes))

    fps = settings.video.fps
    m_start = settings.composition.margin_start
    m_end = settings.composition.margin_end
    frame_start = -fps * m_start
    frame_end = duration + fps*m_end

    video = Video(os.path.join(cache, "output"), settings.audio.path,
        settings.audio.start)

    for frame in trange(frame_start, frame_end):
        img = np.zeros((*settings.video.resolution[::-1], 3), dtype=np.uint8)
        render_blocks(settings, img, notes, frame)
        video.write(img)

    logger.info("Compiling video.")
    video.compile(out, settings.video.fps, m_start, settings.video.vcodec)
