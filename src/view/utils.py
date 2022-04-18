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
import random
from typing import Tuple

import cv2
import numpy as np
from tqdm import trange

TMP = "/tmp"


def extract_frames(path: str) -> Tuple[int, str]:
    """
    Save frames to tmp directory.

    :return: Number of frames and directory they are stored in.
        Frames files are ``%d.jpg``, starting from frame 0.
    """
    video = cv2.VideoCapture(path)
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    rand = str(random.randint(0, 10000000))
    tmpdir = os.path.join(TMP, f"pianoray_viewer_{rand}")
    os.makedirs(tmpdir, exist_ok=True)

    for frame in trange(frames):
        ret, img = video.read()
        if not ret:
            break

        path = os.path.join(tmpdir, f"{frame}.jpg")
        cv2.imwrite(path, img)

    return (frames, tmpdir)
