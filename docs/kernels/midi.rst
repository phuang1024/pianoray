MIDI
====

MIDI parsing and processing kernel.

Input
-----

.. code-block:: json

   {
       "midi": {
           "file": "/path/to/file.mid",
           "fps": 30,
           "capture": [
               "type1",
               "type2",
               "..."
           ],
           "attrs": [
               "type",
               "velocity",
               "..."
           ]
       }
   }

- ``midi``:
    - ``file``: Path to MIDI file to parse.
    - ``fps``: Frames per second of video.
    - ``capture``: List of message types to return.
    - ``attrs``: List of message attributes to include (see output).
      If an attr is absent, no exception is raised. The attr is
      omitted from the output.

Output
------

.. code-block:: json

   {
       "midi": [
           {
               "type": "note_on",
               "time": 123,
               "..."
           },
           "..."
       ]
   }

- ``midi``: List of captured messages.
    - Message attributes.
    - ``time`` attribute is replaced with absolute time in frames,
      first message is frame 0.
