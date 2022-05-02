from typing import Any, Iterable, Set

from .keyframe import Keyframe, Interps


class Property:
    """
    Property base class.
    """
    name: str
    description: str

    animatable: bool
    supported_interps: Iterable[str]

    default: Any

    _keyframes: Set[Keyframe]
    _value: Any

    def __init__(self, name: str, description: str, default: Any,
            animatable: bool) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.animatable = animatable
        self.supported_interps = supported_interps

        self._keyframes = set()
        self._value = default

        assert self.verify(default)

    def animate(self, keyframe: Keyframe) -> None:
        assert self.animatable
        assert keyframe.interp in self.supported_interps
        assert self.verify(keyframe.value)
        self._keyframes.add(keyframe)

    def verify(self, value: Any) -> bool:
        """
        Check whether the value can be assigned to this prop, e.g.
        min and max.
        Override in subclass, if applicable.
        """
        return True

    def value(self, frame) -> Any:
        # TODO
        pass


class BoolProp(Property):
    """
    Boolean.
    """
    supported_interps = {Interps.CONSTANT}


class IntProp(Property):
    """
    Integer.
    """
    supported_interps = {Interps.CONSTANT, Interps.LINEAR}

    min: int
    max: int

    def __init__(self, name: str, description: str, default: int,
            animatable: bool, min: int = None, max: int = None) -> None:
        super().__init__(name, description, default, animatable)
        self.min = min
        self.max = max
