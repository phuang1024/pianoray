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

import cv2
import numpy as np

from .effect import Effect


class Keyboard(Effect):
    """
    Piano keyboard rendering.
    """

    def __init__(self, settings: Settings, cache: str, libs) -> None:
        super().__init__(settings, cache, libs)

    def render(self, img: np.ndarray, frame: int, notes):
        """
        Render the keyboard.
        """
