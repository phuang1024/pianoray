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
from . import logger
from .kernel import Kernel, KernelWrapper, KernelException
from .utils import Namespace


class BasePipeline:
    """
    Extend off of this class to create your pipeline.
    """

    kernels: Namespace
    """Mapping of loaded kernels."""

    meta: Mapping[str, Any]

    def __init__(self, kernels: Mapping[str, Kernel]) -> None:
        """
        Initialize pipeline.
        Don't override.
        """
        self.kernels = Namespace()
        for key in kernels:
            self.kernels[key] = KernelWrapper(kernels[key])

    def get_meta(self) -> Mapping[str, Any]:
        """
        Override this in your subclass.

        Return metadata. Required fields:

        - ``start``: Frame start, inclusive. Frame 0 is start of first note.
        - ``end``: Frame end, inclusive.
          You can get these values from the ``midi`` kernel.
        - ``res``: Video resolution, ``(width, height)``.
        - ``fps``: Video frames per second.
        """
        raise NotImplementedError("Override this in your subclass.")

    def render_frame(self, frame: int) -> np.ndarray:
        """
        Override this in your subclass.

        Render one frame and return the image as a numpy array.

        :param frame: Frame number.
        :return: np.ndarray shape (height, width, 3), RGB channels.
        """
        raise NotImplementedError("Override this in your subclass.")


def check_version(real, require):
    """
    See if the required version of a pipeline can be used
    with this version.
    """
    # TODO

def render_pipeline(pipe: BasePipeline, out_path: str) -> None:
    """
    Renders each frame.
    """
    meta = pipe.get_meta()
    video = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"),
        meta["fps"], meta["res"])

    for frame in trange(meta["start"], meta["end"]+1):
        try:
            img = pipe.render_frame(frame, meta)
        except KernelException as e:
            logger.error("Stop after KernelException:")
            logger.error(str(e))
            raise

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        video.write(img)

    video.release()
