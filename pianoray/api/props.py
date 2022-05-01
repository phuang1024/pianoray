from typing import Any, Sequence, Set


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

    def __init__(self, name: str, description: str, default: Any,
            animatable: bool, supported_interps: Sequence[str]) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.animatable = animatable
        self.supported_interps = supported_interps

        self._keyframes = set()

    def animate(self, keyframe: Keyframe) -> None:
        assert self.animatable
        self._keyframes.add(keyframe)
