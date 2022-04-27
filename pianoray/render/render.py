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
from ..effects import parse_midi
from ..effects import Blocks, Keyboard, Glare
from ..settings import Settings
from .lib import load_libs
from .video import Video


def preprocess(settings: Settings):
    """
    Does stuff to settings, e.g. change coords to pixels.
    """
    coord = settings.video.resolution[0] / 52
    settings.blocks.radius *= coord
    settings.glare.radius *= coord
    settings.keyboard.below_length *= coord

    assert settings.glare.streaks <= 20


def render_video(settings: Settings, out: str, cache: str) -> None:
    preprocess(settings)
    try:
        libs = load_libs(cache)
    except AssertionError:
        logger.error("Failed to build libraries.")
        raise

    for sub in ("glare",):
        os.makedirs(os.path.join(cache, sub), exist_ok=True)

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

    video = Video(os.path.join(cache, "output"), settings.audio.file,
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
    # Parse MIDI.
    notes = parse_midi(settings)
    duration = int(max(x.end for x in notes))

    # Calculate start and end.
    fps = settings.video.fps
    m_start = settings.composition.margin_start
    m_end = settings.composition.margin_end
    frame_start = -fps * m_start
    frame_end = duration + fps*m_end

    # OOP effects
    blocks = Blocks(settings, cache, libs)
    keyboard = Keyboard(settings, cache, libs)
    glare = Glare(settings, cache, libs, notes)

    # Render
    num_frames = 0
    for frame in trange(frame_start, frame_end, desc="Rendering"):
        num_frames += 1
        with open(os.path.join(cache, "currently_rendering.txt"), "w") as fp:
            fp.write(str(frame))

        if real_start is not None and frame < real_start:
            continue

        img = np.zeros((*settings.video.resolution[::-1], 3), dtype=np.uint8)

        blocks.render(settings, img, frame, notes)
        keyboard.render(settings, img, frame)
        glare.render(settings, img, frame, notes)

        video.write(img)

    return num_frames
