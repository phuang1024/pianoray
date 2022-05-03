from typing import Mapping

from .pgroup import PropertyGroup


class Scene:
    """
    Group of PropertyGroups.

    Create a subclass with your pgroups.
    """
    _pgroups: Mapping[str, PropertyGroup]

    def __getattr__(self, name: str) -> PropertyGroup:
        return self._pgroups[name]

    def setup(self) -> None:
        """
        Do any animation or property value setting here.
        """
