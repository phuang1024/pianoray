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

from .video import Video
from .settings import Settings


def render_video(settings: Settings, out: str, cache: str) -> None:
    os.makedirs(cache, exist_ok=True)

    v = Video(cache)
    for i in trange(255):
        img = np.empty((1080, 1920, 3), dtype=np.uint8)
        img[...] = i
        v.save(img)

    v.compile(out, 30)
