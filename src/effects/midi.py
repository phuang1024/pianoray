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

import os
from typing import Sequence, Tuple

import mido

from ..settings import Settings


def parse_midi(settings: Settings) -> Sequence[Tuple[float, float]]:
    """
    Parse midi file.

    :param settings: Settings.
    :return: List of ``(note, velocity, start_frame, end_frame)``.
    """
    path = settings.midi.file
    if path is None or not os.path.isfile(path):
        raise ValueError("Setting midi.file invalid.")

    midi = mido.MidiFile(path)
    notes = []

    t = 0
    started = False
    starts = [0] * 255
    for msg in midi:
        if started:  # Only increment after first note
            t += msg.time * settings.video.fps / settings.midi.speed

        if msg.type.startswith("note_"):
            started = True

            vel = msg.velocity
            note = msg.note - 21
            if msg.type == "note_on" and vel > 0:
                starts[note] = t
            else:
                notes.append((note, vel, starts[note], t))

    return notes
