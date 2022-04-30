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
