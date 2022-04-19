#
#  PianoRay
#  Piano performance visualizer.
#  Copyright  PianoRay Authors  2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from typing import Any, Mapping


class Settings:
    """
    Settings.
    """

    _data: Mapping[str, Any]

    def __init__(self, data: Mapping[str, Any]) -> None:
        object.__setattr__(self, "_data", {})
        for key in data:
            obj = data[key]
            if isinstance(obj, dict):
                obj = Settings(obj)
            self._data[key] = obj

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Settings object has no attribute {name}")

    def __setattr__(self, name: str, value: Any) -> None:
        self._data[name] = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Settings):
            return False
        return self._data == other._data

    def _merge(self, other: "Settings") -> None:
        """
        Merge other settings with self, keeping self if conflict.
        """
        for key in other:
            obj = getattr(other, key)
            if not hasattr(self, key):
                self._data[key] = obj
            else:
                if isinstance(obj, Settings):
                    getattr(self, key)._merge(obj)

    def _json(self) -> Mapping[str, Any]:
        ret = {}
        for key in self._data:
            obj = self._data[key]
            if isinstance(obj, Settings):
                obj = obj._json()
            ret[key] = obj

        return ret
