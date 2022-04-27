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
from typing import Any, Mapping, Sequence

import mido

from ..settings import Settings


class Note:
    """
    One note.
    start and end times are in frames.
    attrs is mapping of arbitrary attributes any effect can set.
    """
    note: int
    velocity: int
    start: float
    end: float
    attrs: Mapping[str, Any]

    def __init__(self, note, velocity, start, end):
        self.note = note
        self.velocity = velocity
        self.start = start
        self.end = end
        self.attrs = {}


def parse_midi(settings: Settings) -> Sequence[Note]:
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
                notes.append(Note(note, vel, starts[note], t))

    return notes
