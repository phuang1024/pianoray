from typing import Any

from .accessor import Accessor


class Modifier:
    """
    Base modifier class. A modifier instance can be called,
    and modifies a value. Examples include multiplying by 0.5
    to dim colors (a Dim modifier).

    Base class modifier does nothing.
    """

    def __init__(self):
        pass

    def __call__(self, default: Accessor, value: Any) -> Any:
        """
        Modify the value.

        :param default: Default values, if you need any.
        :param value: The value to modify.
        """
        return value


class Coords(Modifier):
    """
    Modifier from coords value to pixel value.
    """

    def __call__(self, default, value):
        coord = default.video.resolution[0] / 52
        return value * coord


class SecToFrame(Modifier):
    """
    Convert seconds to frames.
    """

    def __call__(self, default, value):
        return value / default.video.fps
