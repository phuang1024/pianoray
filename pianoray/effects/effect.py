import ctypes
from pathlib import Path
from typing import Mapping

import numpy as np

from ..api.accessor import Accessor


class Effect:
    """
    Base class for all effects.
    """
    cache: Path
    libs: Mapping[str, ctypes.CDLL]
    notes_str: np.ndarray

    def __init__(self, props: Accessor, cache: Path, libs,
            notes_str) -> None:
        self.cache = cache
        self.libs = libs
        self.notes_str = notes_str

    def render(self, props: Accessor, img: np.ndarray, frame: int,
            *args, **kwargs) -> None:
        """
        Override this in the subclass.
        """
        raise NotImplementedError("Override Effect.render")
