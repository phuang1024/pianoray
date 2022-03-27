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

import mido


def length(inp):
    midi = mido.MidiFile(inp["file"])
    fps = inp["fps"]

    first = None
    last = None
    time = 0
    for msg in midi:
        time += msg.time * fps

        if msg.type.startswith("note_"):
            if msg.type == "note_on" and msg.velocity > 0:
                if first is None:
                    first = time
            else:
                last = time

    if first is None or last is None:
        return 0
    return last - first
