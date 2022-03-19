#
#  PianoRay
#  Video rendering pipeline with piano visualization.
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

import numpy as np
import cv2
from tqdm import trange
from typing import Any, Mapping
from .kernel import Kernel


class BasePipeline:
    """
    Extend off of this class to create your pipeline.
    """

    kernels: Mapping[str, Kernel]
    """Mapping of loaded kernels."""

    meta: Mapping[str, Any]
    """
    Metadata. Define in subclass.
    * start: Frame start, inclusive
    * end: Frame end, inclusive
    * res: Video resolution, (width, height)
    * fps: Video frames per second
    """

    def __init__(self, kernels):
        self.kernels = kernels

    def render_frame(self, frame: int) -> np.ndarray:
        """
        Override this in your subclass.
        Render one frame and return the image as a numpy array.

        :param frame: Frame number.
        :return: np.ndarray shape (height, width, 3), RGB channels.
        """
        raise NotImplementedError("Override this in your subclass.")

    def render(self, out_path: str):
        """
        Renders each frame.
        Don't override.
        """
        video = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"),
            self.meta["fps"], self.meta["res"])

        for frame in trange(self.meta["start"], self.meta["end"]+1):
            img = self.render_frame(frame)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            video.write(img)

        video.release()