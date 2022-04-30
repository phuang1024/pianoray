import os
import random
from threading import Thread

import cv2
import numpy as np

from .utils import TMP


class Video:
    """
    Handles extracting and managing frames.
    Saves to tmp directory and extracts in the background.
    """

    run: bool
    tmpdir: str
    fps: int
    num_frames: int
    extracted: int

    def __init__(self, path: str):
        """
        :param path: Path to video.
        """
        self.run = True
        self.extracted = 0

        rand = str(random.randint(0, 10000000))
        self.tmpdir = os.path.join(TMP, f"pianoray_viewer_{rand}")
        os.makedirs(self.tmpdir, exist_ok=True)

        self._video = cv2.VideoCapture(path)
        self.fps = self._video.get(cv2.CAP_PROP_FPS)
        self.num_frames = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))

        Thread(target=self.extract).start()

    def get(self, frame: int) -> np.ndarray:
        """
        Get the frame image.

        :return: np array if successful, None else.
        """
        if frame > self.extracted:
            return None

        path = os.path.join(self.tmpdir, f"{frame}.jpg")
        return cv2.imread(path)

    def extract(self):
        """
        Extract all the frames.
        Run this in a different thread.
        Set self.run to False to stop.
        """
        for frame in range(self.num_frames):
            if not self.run:
                break
            ret, img = self._video.read()
            if not ret:
                break

            path = os.path.join(self.tmpdir, f"{frame}.jpg")
            cv2.imwrite(path, img)

            self.extracted = frame
