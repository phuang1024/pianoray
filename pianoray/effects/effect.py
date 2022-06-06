import ctypes
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

from ..api.accessor import Accessor
from ..cpp import Types
from ..midi import Note, serialize_midi


class Effect:
    """
    Base class for all effects.
    """
    cache: Path
    libs: Mapping[str, ctypes.CDLL]
    notes: Sequence[Note]
    notes_str: np.ndarray

    def __init__(self, props: Accessor, cache: Path, libs,
            notes: Sequence[Note]) -> None:
        self.cache = cache
        self.libs = libs
        self.notes = notes
        self.notes_str = Types.cstr(serialize_midi(notes))

    def render(self, props: Accessor, img: np.ndarray, frame: int,
            *args, **kwargs) -> None:
        """
        Override this in the subclass.
        """
        raise NotImplementedError("Override Effect.render")
