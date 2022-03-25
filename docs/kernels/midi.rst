MIDI
====

MIDI parsing and processing kernel.

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
            "...",
        ],
    }

- ``midi``: List of filtered MIDI messages.
    - ``time``: The time attribute is replaced with absolute time in
      frames, with the first message at frame 0.
    - All other captured attributes of the message.
