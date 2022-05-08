import ctypes
from typing import Mapping

import numpy as np

from ..api.accessor import Accessor


class Effect:
    """
    Base class for all effects.
    """
    cache: str
    libs: Mapping[str, ctypes.CDLL]

    def __init__(self, props: Accessor, cache: str, libs) -> None:
        self.cache = cache
        self.libs = libs

    def render(self, props: Accessor, img: np.ndarray, frame: int,
            *args, **kwargs) -> None:
        """
        Override this in the subclass.
        """
        raise NotImplementedError("Override Effect.render")
