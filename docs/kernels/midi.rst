MIDI
====

MIDI parsing and processing kernel.

Length
------

Compute the length of the MIDI file from the start of the first note
to the end of the last note.

Input
^^^^^

.. code-block:: json

    {
        "midi": {
            "type": "length",
            "file": "/path/to/file.mid",
            "fps": 30
        }
    }

- ``midi``:
    - ``type``: Must be ``"length"`` to specify operation.
    - ``file``: Path to MIDI file.
    - ``fps``: Frames per second.

Output
^^^^^^

.. code-block:: json

    {
        "midi": 123
    }

- ``midi``: Length of MIDI file in frames.

Filter
------

This operation filters a MIDI file for messages of a given type.

Input
^^^^^

.. code-block:: json

    {
        "midi": {
            "type": "filter",
            "file": "/path/to/file.mid",
            "fps": 30,
            "types": [
                "msg_type_1",
                "note_on",
                "control_change",
                "..."
            ],
            "attrs": [
                "note",
                "velocity",
                "control",
                "..."
            ]
        }
    }

- ``midi``:
    - ``type``: Must be ``"filter"`` to specify operation.
    - ``file``: Path to MIDI file.
    - ``fps``: Frames per second.
    - ``types``: List of message types to accept.
    - ``attrs``: List of message attributes to return. If a message
      does not have a requested attribute, it is omitted and no error
      is raised.

Output
^^^^^^

.. code-block:: json

    {
        "midi": [
            {
                "time": 1,
                "note": 20,
                "...": "..."
            }
            "..."
        ]
    }

- ``midi``: List of filtered MIDI messages.
    - ``time``: The time attribute is replaced with absolute time in
      frames, with the first message at frame 0.
    - All other captured attributes of the message.

Blocks
------

For each time a note is pressed, record start frame, end frame, and velocity.

Input
^^^^^

.. code-block:: json

    {
        "midi": {
            "type": "blocks",
            "file": "/path/to/file.mid",
            "fps": 30
        }
    }

- ``midi``:
    - ``type``: Must be ``"blocks"`` to specify operation.
    - ``file``: Path to MIDI file.
    - ``fps``: Frames per second.

Output
^^^^^^

.. code-block:: json

    {
        "midi": [
            [1, 12, 65, 30],
            "..."
        ]
    }

- ``midi``: List of note infos.
    - Each note is ``[note_num, start_frame, end_frame, velocity]``. Start
      frame is the frame the note starts playing, and end frame is the frame
      the note stops.
