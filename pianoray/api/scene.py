from typing import Any, Mapping, Type

from .pgroup import PropertyGroup


class Scene:
    """
    Group of PropertyGroups.

    Create a subclass with your pgroups. Set the dictionary ``_pgroups`` to
    mapping of id to property group class (not instance). The dictionary
    ``_pgroups_real`` is automatically created on init and contains instances
    of ``_pgroups``.

    .. code-block:: py

        class MyScene(Scene):
            _pgroups = {
                "food": FoodProps,
            }

    Create a subclass of a scene, and override the setup method to do animation.
    Scene.setup is called at initialize time.

    .. code-block:: py

        # We are extending "MyScene", described above.
        class MyOtherScene(MyScene):
            def setup(self):
                self.food.temperature = 100
    """
    _pgroups: Mapping[str, Type[PropertyGroup]]
    _pgroups_real: Mapping[str, PropertyGroup]

    def __init__(self):
        """
        Initializes pgroups.
        """
        for k, v in _pgroups.items():
            _pgroups_real[k] = v()

        self.setup()

    def __getattr__(self, name: str) -> PropertyGroup:
        return self._pgroups_real[name]

    def _values(self, frame: int) -> Mapping[str, Mapping[str, Any]]:
        """
        Returns dict of values of all pgroups at frame.
        """
        ret = {}
        for k, pgroup in self._pgroups_real.items():
            v = pgroup._values(frame)
            ret[k] = v

        return ret

    def setup(self) -> None:
        """
        Do any animation or property value setting here.
        """
