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

import json
import mido


def filter_midi(inp):
    out = {"midi": []}

    midi = mido.MidiFile(inp["file"])
    fps = inp["fps"]
    types = inp["types"]
    attrs = inp["attrs"]

    time = 0  # Frames
    for msg in midi:
        time += msg.time * fps
        if msg.type in types:
            msg_out = {"time": time}
            for attr in attrs:
                if attr != "time" and hasattr(msg, attr):
                    msg_out[attr] = getattr(msg, attr)
            out["midi"].append(msg_out)

    return out
