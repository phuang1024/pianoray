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
from pathlib import Path
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
    settings.blocks.glow_radius *= coord
    settings.glare.radius *= coord
    settings.keyboard.below_length *= coord

    assert settings.glare.streaks <= 20


def check_previous(args, settings, cache):
    """
    Check if continue previous render.

    :return: Frame to start rendering from.
    """
    cache_settings = cache / "settings.json"
    cache_curr = cache / "currently_rendering.txt"

    real_start = None
    if cache_settings.is_file() and cache_curr.is_file():
        with open(cache_settings, "r") as fp:
            prev_sets = Settings(json.load(fp))

        if prev_sets == settings:
            with open(cache_curr, "r") as fp:
                data = fp.read()
                real_start = int(data) if data.isdigit() else None

            if real_start is not None:
                if args.resume is None:
                    print("Last render has same settings as this render, "
                          f"and stopped at frame {real_start}.")
                    if input("Continue last render? [Y/n] ").lower().strip() \
                            == "n":
                        real_start = None

                elif not args.resume:
                    real_start = None

    return real_start


def render_video(args, settings: Settings, out: str, cache: Path) -> None:
    """
    Render system main.

    :param args: Argparse arguments.
    """
    # Preprocessing
    preprocess(settings)
    try:
        libs = load_libs(cache)
    except AssertionError:
        logger.error("Failed to build libraries.")
        raise

    # Cache subdirs
    for sub in ("glare",):
        (cache/sub).mkdir(exist_ok=True)

    # Save settings to cache.
    os.makedirs(cache, exist_ok=True)
    real_start = check_previous(args, settings, cache)
    with open(cache / "settings.json", "w") as fp:
        json.dump(settings._json(), fp)

    video = Video(cache/"output", settings.audio.file,
        settings.audio.start)
    num_frames = render_frames(settings, libs, video, cache, real_start)
    video.compile(out, settings.video.fps, num_frames,
        settings.composition.margin_start, settings.video.vcodec)


def render_frames(settings, libs, video, cache, real_start=None) -> int:
    """
    Render frames.

    :param real_start: Frame to start rendering from.
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
    if real_start is None:
        real_start = frame_start
    logger.info(f"Starting render from frame {real_start}")

    num_frames = real_start - frame_start
    video.frame = num_frames
    for frame in trange(real_start, frame_end, desc="Rendering"):
        num_frames += 1
        with open(cache/"currently_rendering.txt", "w") as fp:
            fp.write(str(frame))

        img = np.zeros((*settings.video.resolution[::-1], 3), dtype=np.uint8)

        blocks.render(settings, img, frame, notes)
        keyboard.render(settings, img, frame)
        glare.render(settings, img, frame, notes)

        video.write(img)

    return num_frames
