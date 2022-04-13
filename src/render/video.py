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
import shutil
from subprocess import Popen, PIPE
from typing import Sequence

import cv2
import numpy as np

from .. import logger
from ..utils import FFMPEG


class Video:
    """
    Video.

    Saves frames to given cache directory and uses ffmpeg to make the
    final video.
    """

    def __init__(self, cache: str, audio: str = None,
            audio_offset: float = 0) -> None:
        """
        Initializes video.

        :param cache: Cache directory. Frames stored there.
        :param audio: Path to audio file.
        :param audio_offset: Seconds. Positive values play audio later.
        """
        self.cache = cache
        self.audio = audio
        self.audio_offset = audio_offset
        self.frame = 0

        os.makedirs(os.path.join(self.cache, "frames"), exist_ok=True)

    def write(self, img: np.ndarray) -> int:
        """
        Write a frame.
        Converts from RGB to BGR.

        :param img: Frame of shape ``(height, width, 3)``
        :return: This frame number.
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        path = os.path.join(self.cache, "frames", str(self.frame)+".jpg")
        cv2.imwrite(path, img)

        self.frame += 1
        return self.frame - 1

    def compile(self, out: str, fps: int, num_frames: int,
            margin_start: float, vcodec="libx265", crf=24) -> None:
        """
        Use ffmpeg to compile frames and audio to video.

        :param out: Output video path.
        :param fps: Frames per second.
        :param num_frames: Total number of frames to compile.
        :param margin_start: settings.composition.margin_start
        :param vcodec: Video codec. Use libx264 if libx265 fails.
        :param crf: Constant rate factor. Higher values produce smaller
            file sizes but lower quality.
        """
        # Frames to video
        logger.info("Compiling frames to video.")
        args = [
            FFMPEG,
            "-y",
            "-i", os.path.join(self.cache, "frames", "%d.jpg"),
            "-vframes", num_frames,
            "-c:v", vcodec,
            "-crf", crf,
            "-r", fps,
            os.path.join(self.cache, "no_audio.mp4"),
        ]
        run_ffmpeg(args)

        if self.audio is not None:
            # Cut audio
            logger.info("Processing audio.")
            args = [
                FFMPEG,
                "-y",
                "-ss", self.audio_offset-margin_start, "-t", 100000,
                "-i", self.audio,
                os.path.join(self.cache, "offset.mp3"),
            ]
            run_ffmpeg(args)

            # Mix
            logger.info("Combining audio and video.")
            args = [
                FFMPEG,
                "-y",
                "-i", os.path.join(self.cache, "no_audio.mp4"),
                "-i", os.path.join(self.cache, "offset.mp3"),
                "-c", "copy",
                out,
            ]

            run_ffmpeg(args)

        else:
            # Copy to output.
            shutil.copy(os.path.join(self.cache, "no_audio.mp4"), out)

        logger.info(f"Video saved to {out}")


def run_ffmpeg(args: Sequence[str]):
    args = list(map(str, args))
    proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.wait()

    if (code := proc.returncode) != 0:
        msg = f"FFmpeg exited with code {code}. " + \
            "Command: " + " ".join(args)
        raise ValueError(msg)
