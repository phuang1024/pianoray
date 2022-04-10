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


def is_white_key(key: int) -> bool:
    """
    If the key is a white key on piano.
    """
    return (key % 12) in (1, 4, 6, 9, 11)

def key_pos(key: int) -> float:
    """
    Position of the center of the key on the keyboard.
    Factor from 0 to 1 (start of first key to end of last).
    """
    white_width = 1 / 88

    last_white = False  # Last key was white
    pos = 0
    for k in range(key):
        white = is_white_key(k)
        if white:
            if last_white:
                pos += white_width
            else:
                pos += white_width / 2
        else:
            pos += white_width / 2

    return pos
