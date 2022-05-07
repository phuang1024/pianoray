from typing import Any, Mapping, Optional

from .accessor import Accessor
from .props import Property


class PropertyGroup:
    """
    Group of properties. Define a subclass to create your PropertyGroup.
    Define properties by creating annotations with ``:``. Don't override
    any methods, as instancing a PropertyGroup subclass requires the
    methods.

    .. code-block:: py

        class MyProps(PropertyGroup):
            temperature: FloatProp(
                name="Temperature",
                desc="Temperature to cook the food at.",
                default=-10,
            )

            food: StringProp(
                name="Food",
                desc="The food to cook.",
                default="Java",
            )

    You can set and get properties.

    .. code-block:: py

        pgroup.temperature                # Returns the property object.
        pgroup.temperature.animate(...)   # Animate. See Property docs.
        pgroup.temperature = -273         # Calls pgroup.temperature.set_value()
    """

    _props: Mapping[str, Property]

    def __init__(self):
        """
        Reads __annotations__ and stores in ``self._props``.
        """
        object.__setattr__(self, "_props", {})

        for k, v in self.__annotations__.items():
            if isinstance(v, Property):
                self._props[k] = v

    def __setattr__(self, name: str, value: Any):
        """
        ``pgroup.prop_name = 1``
        is equivalent to
        ``pgroup.prop_name.set_value(1)``
        """
        self._props[name].set_value(value)

    def __getattr__(self, name: str) -> Property:
        return self._props[name]

    def _values(self, frame: int, use_mods: bool = True,
            default: Optional[Accessor] = None) -> Mapping[str, Any]:
        """
        Get values of all properties at frame.
        Returns ``{"prop_name": value}``.
        """
        ret = {}
        for k, prop in self._props.items():
            v = prop.value(frame, use_mods, default)
            ret[k] = v

        return ret
