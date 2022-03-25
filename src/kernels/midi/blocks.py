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


def compute_blocks(inp):
    out = {"midi": []}
    notes = [None] * 256

    midi = mido.MidiFile(inp["file"])
    fps = inp["fps"]

    time = 0  # Frames
    for msg in midi:
        time += msg.time * fps

        if msg.type.startswith("note_"):
            note = msg.note
            vel = msg.velocity
            if msg.type == "note_on" and msg.velocity > 0:
                if notes[note] is not None:
                    out["midi"].append((note, notes[note], time, vel))
                notes[note] = time
            else:
                out["midi"].append((note, notes[note], time, vel))
                notes[note] = None

    return out
