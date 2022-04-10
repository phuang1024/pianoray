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

Available
---------

Most settings have default values. See ``src/utils.py`` for the default
settings.

Colors are ``[R, G, B]`` from 0 to 255.

- ``fps``: Frames per second.
- ``resolution``: Video resolution ``[width, height]``.
- ``vcodec``: Video codec. This will be passed to FFmpeg, so please
  provide a value that FFmpeg recognizes, e.g. ``libx264``.
- ``composition``:
    - ``margin_start``: Seconds of video before the first note.
    - ``margin_end``: Seconds of video after the last note ends.
- ``piano``:
    - ``black_width_fac``: Black key width as factor of white key width.
- ``blocks``:
    - ``speed``: If ``X`` is the distance between the top of the screen and the
      top of the keyboard, the blocks travel ``speed * X`` per second.
    - ``color``: RGB color of the blocks.
    - ``radius``: Block corner rounding radius.
- ``midi``:
    - ``file``: Path to MIDI file.
    - ``speed``: Speed multiplier.
