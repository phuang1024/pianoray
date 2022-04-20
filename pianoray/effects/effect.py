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

import ctypes
from typing import Mapping

import numpy as np

from ..settings import Settings


class Effect:
    """
    Base class for all effects.
    """

    settings: Settings
    cache: str
    libs: Mapping[str, ctypes.CDLL]

    def __init__(self, settings: Settings, cache: str, libs) -> None:
        self.settings = settings
        self.cache = cache
        self.libs = libs

    def render(self, settings: Settings, img: np.ndarray,
            frame: int, *args, **kwargs) -> None:
        """
        Override this in the subclass.
        """
        raise NotImplementedError("Override Effect.render")
