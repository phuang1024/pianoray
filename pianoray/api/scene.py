from typing import Any, Mapping, Type

from .accessor import Accessor
from .pgroup import PropertyGroup


class Scene:
    """
    Group of PropertyGroups.

    Create a subclass with your pgroups. Set the dictionary ``_pgroups`` to
    mapping of id to property group instance.

    .. code-block:: py

        class MyScene(Scene):
            _pgroups = {
                "food": FoodProps(),
            }

    Create a subclass of a scene, and override the setup method to do animation.
    Scene.setup is called at initialize time.

    .. code-block:: py

        # We are extending "MyScene", described above.
        class MyOtherScene(MyScene):
            def setup(self):
                self.food.temperature = 100
    """
    _pgroups: Mapping[str, PropertyGroup]

    def __init__(self):
        """
        Initializes pgroups.
        """
        self.setup()

    def __getattr__(self, name: str) -> PropertyGroup:
        if name == "default":
            return object.__getattribute__(self, "default")
        return object.__getattribute__(self, "_pgroups")[name]

    def values(self, frame: int, use_mods: bool = True) -> Accessor:
        """
        Returns Accesor object of all pgroup values at frame.
        """
        default = self.values(0, False) if use_mods else None

        ret = {}
        for k, pgroup in self._pgroups.items():
            v = pgroup._values(frame, use_mods, default)
            ret[k] = v

        return Accessor(ret)

    @property
    def default(self) -> Accessor:
        """
        Equivalent to ``self.values(0)``.
        Usually used to get non animatable props.
        """
        return self.values(0)

    def setup(self) -> None:
        """
        Do any animation or property value setting here.
        """
