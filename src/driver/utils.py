#
#  PianoRay
#  Video rendering pipeline with piano visualization.
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

from io import BytesIO
from typing import Any, Mapping


class Namespace:
    """
    General getattr and setattr object stuff.
    """

    _items: Mapping[str, Any]

    def __init__(self) -> None:
        object.__setattr__(self, "_items", {})

    def __hasattr__(self, attr: str) -> bool:
        return attr in self._items

    def __getattr__(self, attr: str) -> Any:
        return self._items[attr]

    def __setattr__(self, attr: str, val: Any) -> None:
        self._items[attr] = val

    def __contains__(self, attr: str) -> bool:
        return attr in self._items

    def __getitem__(self, attr: str) -> Any:
        return self._items[attr]

    def __setitem__(self, attr: str, val: Any) -> None:
        self._items[attr] = val


def readall(stream: BytesIO) -> bytes:
    """
    Read all from an output bytes stream.
    """
    out = b""
    while len(chunk := stream.read(1024)) > 0:
        out += chunk
    return out
