"""
Video writer.
"""

import os
import shutil
from pathlib import Path
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

    def __init__(self, cache: Path) -> None:
        """
        Initializes video.

        :param cache: Cache directory. Frames stored there.
        """
        self.cache = cache
        self.frame = 0

        (self.cache/"frames").mkdir(parents=True, exist_ok=True)

    def write(self, img: np.ndarray) -> int:
        """
        Write a frame.
        Converts from RGB to BGR.

        :param img: Frame of shape ``(height, width, 3)``
        :return: This frame number.
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        path = str(self.cache / "frames" / f"{self.frame}.jpg")
        cv2.imwrite(path, img)

        self.frame += 1
        return self.frame - 1

    def compile(self, out: str, props) -> None:
        """
        Use ffmpeg to compile frames and audio to video.

        :param out: Output video path.
        """
        # Frames to video
        logger.info("Compiling frames to video.")
        args = [
            FFMPEG,
            "-y",
            "-r", props.video.fps,
            "-start_number", 0,
            "-i", self.cache / "frames" / "%d.jpg",
            "-vframes", self.frame,
            "-c:v", props.video.vcodec, "-an",
            "-crf", 24,
            "-r", props.video.fps,
            self.cache / "no_audio.mp4",
        ]
        run_ffmpeg(args)

        if props.audio.file is not None:
            # Cut audio
            logger.info("Processing audio.")
            args = [
                FFMPEG,
                "-y",
                "-ss", props.audio.start - props.composition.margin_start,
                "-t", self.frame / props.video.fps,
                "-i", props.audio.file,
                self.cache / "offset.mp3",
            ]
            run_ffmpeg(args)

            # Mix
            logger.info("Combining audio and video.")
            args = [
                FFMPEG,
                "-y",
                "-i", self.cache / "no_audio.mp4",
                "-i", self.cache / "offset.mp3",
                "-c", "copy",
                out,
            ]

            run_ffmpeg(args)

        else:
            # Copy to output.
            shutil.copy(self.cache / "no_audio.mp4", out)

        logger.info(f"Video saved to {out}")


def run_ffmpeg(args: Sequence[str]):
    args = list(map(str, args))
    proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.wait()

    if proc.returncode != 0:
        msg = f"FFmpeg exited with code {proc.returncode}. " + \
            "Command: " + " ".join(args)
        raise ValueError(msg)
