from typing import Any, Sequence, Set

from .keyframe import Keyframe


class Property:
    """
    Property base class.
    """
    name: str
    description: str

    animatable: bool
    supported_interps: Sequence[str]

    default: Any

    _keyframes: Set[Keyframe]
    _value: Any

    def __init__(self, name: str, description: str, default: Any,
            animatable: bool, supported_interps: Sequence[str]) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.animatable = animatable
        self.supported_interps = supported_interps

        self._keyframes = set()
        self._value = default

    def animate(self, keyframe: Keyframe) -> None:
        assert self.animatable
        assert keyframe.interp in self.supported_interps
        self._keyframes.add(keyframe)

    def value(self, frame) -> Any:
        pass
