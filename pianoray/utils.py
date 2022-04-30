import os
import shutil
from pathlib import Path

VERSION = "0.1.0"

ROOT = Path(__file__).absolute().parent

FFMPEG = shutil.which("ffmpeg")
GCC = shutil.which("g++")
assert FFMPEG is not None
assert GCC is not None


SETTINGS_DEFAULT = {
    "video": {
        "fps": 30,
        "resolution": (1920, 1080),
        "vcodec": "libx265",
    },
    "audio": {
        "file": None,
        "start": 0,
    },
    "composition": {
        "margin_start": 3,
        "margin_end": 3,
        "fade_in": 1,
        "fade_out": 1,
        "fade_blur": 1,
    },
    "piano": {
        "black_width_fac": 0.6,
    },
    "blocks": {
        "speed": 0.5,
        "color": [150, 160, 240],
        "radius": 0.25,
        "glow_intensity": 0.3,
        "glow_color": [230, 230, 255],
        "glow_radius": 0.4,
    },
    "midi": {
        "file": None,
        "speed": 1,
        "min_length": 0.08,
    },
    "keyboard": {
        "file": None,
        "start": 0,
        "crop": None,
        "dim_mult": 1,
        "dim_add": 0,
        "below_length": 7,
        "octave_lines": True,
    },
    "glare": {
        "radius": 3,
        "intensity": 0.9,
        "jitter": 0.08,
        "streaks": 6,
    }
}


def forever():
    """
    Generator for indefinite tqdm progressbar.
    """
    while True:
        yield


def bounds(v, vmin, vmax):
    """
    Bound v between vmin and vmax.
    """
    return min(max(v, vmin), vmax)
