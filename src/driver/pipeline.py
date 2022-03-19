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
from typing import Mapping, Tuple
from .kernel import Kernel


class BasePipeline:
    """
    Extend off of this class to create your pipeline.
    """
    kernels: Mapping[str, Kernel]

    def __init__(self, kernels):
        self.kernels = kernels

    def render_frame(self, frame: int) -> np.ndarray:
        """
        Render one frame and return the image as a numpy array.
        Override this in your subclass.
        """
        raise NotImplementedError("Override this in your subclass.")

    def get_frame_bounds(self) -> Tuple[int, int]:
        """
        Return ``(start_frame, end_frame)``, inclusive.
        Override this in your subclass.
        """
        raise NotImplementedError("Override this in your subclass.")

    def render(self, out_path: str):
        """
        Renders each frame.
        Don't override.
        """
        start, end = self.get_frame_bounds()
        self.render_frame(0)
