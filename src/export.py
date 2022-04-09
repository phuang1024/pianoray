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
from subprocess import Popen, PIPE

import cv2
import numpy as np

from . import logger
from .utils import FFMPEG


class Video:
    """
    Video.

    Saves frames to given cache directory and uses ffmpeg to make the
    final video.
    """

    def __init__(self, cache: str) -> None:
        """
        Initializes video.

        :param cache: Cache directory. Frames stored there.
        """
        self.cache = cache
        self.frame = 0

    def save(self, img: np.ndarray) -> int:
        """
        Save a frame.
        Converts from RGB to BGR.

        :param img: Frame of shape ``(height, width, 3)``
        :return: This frame number.
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        path = os.path.join(self.cache, str(self.frame)+".jpg")
        cv2.imwrite(img, path)

        self.frame += 1
        return self.frame - 1

    def compile(self, out: str, fps: int, vcodec="libx265", crf=24) -> None:
        """
        Use ffmpeg to compile frames to video.

        :param out: Output video path.
        :param fps: Frames per second.
        :param vcodec: Video codec. Use libx264 if libx265 fails.
        :param crf: Constant rate factor. Higher values produce smaller
            file sizes but lower quality.
        """
        args = [
            FFMPEG,
            "-i", "%d.jpg",
            "-c:v", vcodec,
            "-crf", crf,
            "-r", fps,
            out,
        ]

        proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        proc.wait()

        if proc.returncode != 0:
            msg = f"FFmpeg exited with code {proc.returncode} when compiling
                {out}")
            raise ValueError(msg)
