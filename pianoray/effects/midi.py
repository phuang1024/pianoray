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
    min_len = settings.midi.min_length * settings.video.fps

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
                end = t if (t-starts[note]) > min_len else \
                    starts[note] + min_len
                notes.append(Note(note, vel, starts[note], end))

    return notes
