from typing import Any


class Interp:
    """
    Namespace for interpolation types.
    """
    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"
    QUADRATIC = "QUADRATIC"


class Keyframe:
    """
    Animate a property.
    """
    frame: int
    value: Any
    interp: str

    def __init__(self, frame: int, value: Any, interp: str) -> None:
        self.frame = frame
        self.value = value
        self.interp = interp

    def __eq__(self, other):
        return isinstance(other, Keyframe) and self.frame == other.frame

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return isinstance(other, Keyframe) and self.frame < other.frame

    def __gt__(self, other):
        return isinstance(other, Keyframe) and self.frame > other.frame

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

    def __repr__(self) -> str:
        return f"Keyframe(frame={self.frame}, value={self.value}, " + \
               f"interp={self.interp})"
