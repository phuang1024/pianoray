Settings
========

When creating a video, many settings are passed to PianoRay.
The settings should be stored in a JSON file containing dictionaries
of ``name: value`` pairs with nested dictionaries.

Example
-------

Save a JSON file of your settings, and pass to ``pianoray``.

.. code-block:: json

    {
        "fps": 30,
        "resolution": [1920, 1080],
        "midi": {
            "path": "/path/to/file.mid"
        }
    }

Available Settings
------------------

Most settings have default values. See ``src/utils.py`` for the default
settings.

- ``fps``: Frames per second.
- ``resolution``: Video resolution ``[width, height]``.
- ``vcodec``: Video codec. This will be passed to FFmpeg, so please
  provide a value that FFmpeg recognizes, e.g. ``libx264``.
- ``composition``:
    - ``margin_start``: Seconds of video before the first note.
    - ``margin_end``: Seconds of video after the last note ends.
- ``midi``:
    - ``file``: Path to MIDI file.
    - ``speed``: Speed multiplier.
