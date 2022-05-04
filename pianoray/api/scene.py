from typing import Mapping, Type

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
    """
    _pgroups: Mapping[str, Type[PropertyGroup]]
    _pgroups_real: Mapping[str, PropertyGroup]

    def __init__(self):
        """
        Initializes pgroups.
        """
        for k, v in _pgroups.items():
            _pgroups_real[k] = v()

    def __getattr__(self, name: str) -> PropertyGroup:
        return self._pgroups[name]

    def setup(self) -> None:
        """
        Do any animation or property value setting here.
        """
