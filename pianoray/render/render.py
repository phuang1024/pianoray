"""
Rendering pipeline.
"""

import ctypes
import json
import os
from pathlib import Path
from typing import Mapping

import cv2
import numpy as np
from tqdm import trange

from .. import logger
from ..cpp import Types, load_libs
from ..midi import parse_midi, serialize_midi
from ..effects import Blocks, Keyboard, Glare, Particles
from .composite import add_fade, composite
from .video import Video


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
            prev_sets = Settings(json.load(fp))  # TODO change

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


def render_video(args, scene, out: str, cache: Path) -> None:
    """
    Render system main.

    :param args: Argparse arguments.
    """
    # Libraries
    try:
        libs = load_libs(cache)
    except AssertionError:
        logger.error("Failed to build libraries.")
        raise

    # Cache subdirs
    for sub in ("glare", "ptcls"):
        (cache/sub).mkdir(exist_ok=True)

    # Save settings to cache.
    """
    os.makedirs(cache, exist_ok=True)
    real_start = check_previous(args, settings, cache)
    with open(cache / "settings.json", "w") as fp:
        json.dump(settings._json(), fp)
    """
    real_start = None  # Remove later

    props = scene.default
    video = Video(cache / "output")
    render_frames(scene, libs, video, cache, real_start)
    video.compile(out, props)


def get_frame_bounds(props, duration):
    """
    Returns (start_frame, end_frame) of whole video, where frame 0 is
    start of first note.

    :param duration: Duration of MIDI in frames.
    """
    fps = props.video.fps
    m_start = props.comp.margin_start
    m_end = props.comp.margin_end
    frame_start = -fps * m_start
    frame_end = duration + fps*m_end

    return (frame_start, frame_end)


def render_frames(scene, libs, video, cache, real_start=None) -> int:
    """
    Render frames.

    :param real_start: Frame to start rendering from.
    :return: Number of frames rendered.
    """
    # Parse MIDI.
    notes = parse_midi(scene.default)
    duration = int(max(x.end for x in notes))

    # Calculate start and end.
    frame_start, frame_end = get_frame_bounds(scene.default, duration)

    # OOP effects
    props = scene.default
    blocks = Blocks(props, cache, libs, notes)
    keyboard = Keyboard(props, cache, libs, notes)
    #glare = Glare(props, cache, libs, notes)
    #ptcls = Particles(props, cache, libs)

    # Adjust start to match previous render
    if real_start is None:
        real_start = frame_start
    frame_start, frame_end, real_start = map(int,
        (frame_start, frame_end, real_start))
    logger.info(f"Starting render from frame {real_start}")

    # Render
    num_frames = real_start - frame_start
    video.frame = num_frames
    for frame in trange(real_start, frame_end, desc="Rendering"):
        # Save state
        num_frames += 1
        with open(cache/"currently_rendering.txt", "w") as fp:
            fp.write(str(frame))

        # Create image
        shape = (*scene.default.video.resolution[::-1], 3)
        raw_img = np.zeros(shape, dtype=np.float64)

        # Apply effects
        props = scene.values(frame)
        blocks.render(props, raw_img, frame)
        #ptcls.render(props, img, frame, notes)
        #glare.render(props, img, frame, notes)

        # Compositing
        img = composite(libs, props, raw_img)
        keyboard.render(props, img, frame)
        add_fade(scene.default, img, frame_start, frame_end, frame)

        video.write(img)
