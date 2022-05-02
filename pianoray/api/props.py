from typing import Any, Iterable, List

from .keyframe import Keyframe, Interp
from .interpolate import interpolate


class Property:
    """
    Property base class.
    """
    name: str
    desc: str

    animatable: bool
    supported_interps: Iterable[str]

    default: Any

    _keyframes: List[Keyframe]
    _value: Any

    def __init__(self, name: str, desc: str, default: Any,
            animatable: bool) -> None:
        self.name = name
        self.desc = desc
        self.default = default
        self.animatable = animatable

        self._keyframes = []
        self._value = default

        assert self.verify(default)

    def animate(self, keyframe: Keyframe) -> None:
        assert self.animatable
        assert keyframe.interp in self.supported_interps
        assert self.verify(keyframe.value)
        self._keyframes.append(keyframe)

    def verify(self, value: Any) -> bool:
        """
        Check whether the value can be assigned to this prop, e.g.
        min and max.
        Override in subclass, if applicable.
        """
        return True

    def value(self, frame) -> Any:
        keys = sorted(self._keyframes)

        if len(keys) == 0:
            return self._value

        elif len(keys) == 1:
            return keys[0].value

        else:
            if frame <= keys[0].frame:
                return keys[0].value
            elif frame >= keys[-1].frame:
                return keys[-1].value
            else:
                for i, k in enumerate(keys):
                    if k.frame == frame:
                        return k.value
                    if k.frame > frame:
                        break

                k1 = keys[i-1]
                k2 = keys[i]
                return interpolate(k1, k2, frame)


class BoolProp(Property):
    """
    Boolean.
    """
    supported_interps = {Interp.CONSTANT}


class IntProp(Property):
    """
    Integer.
    """
    supported_interps = {Interp.CONSTANT, Interp.LINEAR}

    min: int
    max: int

    def __init__(self, name: str, desc: str, default: int,
            animatable: bool, min: int = None, max: int = None) -> None:
        super().__init__(name, desc, default, animatable)
        self.min = min
        self.max = max


if __name__ == "__main__":
    b1 = BoolProp(name="asdf", desc="desc", default=False, animatable=False)
    b2 = BoolProp(name="asdf", desc="desc", default=False, animatable=True)

    try:
        b1.animate(Keyframe(0, False, Interp.CONSTANT))
    except AssertionError as e:
        print("Cannot animate b1:", e)

    print(b2.value(0))
    b2.animate(Keyframe(0, True, Interp.CONSTANT))
    print(b2.value(0), b2.value(1))
    b2.animate(Keyframe(5, False, Interp.CONSTANT))
    print(b2.value(-1), b2.value(0), b2.value(2), b2.value(5), b2.value(6))

    i = IntProp(name="asdf", desc="desc", default=10, animatable=True)
    print(i.value(0))
    i.animate(Keyframe(0, 5, Interp.LINEAR))
    print(i.value(0))
    i.animate(Keyframe(5, 10, Interp.CONSTANT))
    i.animate(Keyframe(10, 15, Interp.CONSTANT))
    print([i.value(a) for a in range(0, 6)])
    print([i.value(a) for a in range(5, 11)])
