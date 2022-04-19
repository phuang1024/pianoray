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

import ctypes
import json
import os
from typing import Mapping

import numpy as np
from tqdm import trange

from .. import logger
from ..cpp import build_lib, Types
from ..effects import render_blocks
from ..effects import parse_midi
from ..settings import Settings
from .video import Video


def preprocess(settings: Settings):
    """
    Does stuff to settings, e.g. change coords to pixels.
    """
    coord = settings.video.resolution[0] / 52
    settings.blocks.radius *= coord


def load_libs(cache: str) -> Mapping[str, ctypes.CDLL]:
    """
    Load libraries.
    """
    cache = os.path.join(cache, "c_libs")
    os.makedirs(cache, exist_ok=True)

    blocks = build_lib(
        ["effects/blocks/blocks.cpp"],
        cache,
        "blocks",
    )
    blocks.render_blocks.argtypes = [
        Types.img, Types.int, Types.int,
        Types.int,
        Types.int, Types.arr_int, Types.arr_double, Types.arr_double,
        Types.int, Types.double, Types.double, Types.double, Types.arr_uchar,
    ]

    return {
        "blocks": blocks,
    }


def render_video(settings: Settings, out: str, cache: str) -> None:
    preprocess(settings)
    libs = load_libs(cache)

    cache_settings = os.path.join(cache, "settings.json")
    cache_curr = os.path.join(cache, "currently_rendering.txt")

    # Check if continue previous render
    real_start = None
    if os.path.isfile(cache_settings) and os.path.isfile(cache_curr):
        with open(cache_settings, "r") as fp:
            prev_sets = Settings(json.load(fp))

        if prev_sets == settings:
            with open(cache_curr, "r") as fp:
                real_start = int(fp.read())
            print("Last render has same settings as this render, "
                  f"and stopped at frame {real_start}.")
            if input("Continue last render? [Y/n] ").lower().strip() == "n":
                real_start = None

    os.makedirs(cache, exist_ok=True)
    with open(cache_settings, "w") as fp:
        json.dump(settings._json(), fp)

    video = Video(os.path.join(cache, "output"), settings.audio.path,
        settings.audio.start)
    num_frames = render_frames(settings, libs, video, cache, real_start)
    video.compile(out, settings.video.fps, num_frames,
        settings.composition.margin_start, settings.video.vcodec)

    if os.path.isfile(cache_curr):
        os.remove(cache_curr)


def render_frames(settings, libs, video, cache, real_start=None) -> int:
    """
    Render frames.

    :param real_start: If applicable, currently_rendering
    :return: Number of frames rendered.
    """
    notes = parse_midi(settings)
    duration = int(max(x[3] for x in notes))

    fps = settings.video.fps
    m_start = settings.composition.margin_start
    m_end = settings.composition.margin_end
    frame_start = -fps * m_start
    frame_end = duration + fps*m_end

    num_frames = 0
    for frame in trange(frame_start, frame_end):
        num_frames += 1
        with open(os.path.join(cache, "currently_rendering.txt"), "w") as fp:
            fp.write(str(frame))

        if real_start is not None and frame < real_start:
            continue

        img = np.zeros((*settings.video.resolution[::-1], 3), dtype=np.uint8)
        render_blocks(libs["blocks"], settings, img, notes, frame)
        video.write(img)

    return num_frames
