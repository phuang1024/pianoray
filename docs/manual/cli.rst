CLI
===

Command line interface arguments.

Type ``pianoray -h`` for info.

Example Commands
----------------

- Render: ``pianoray render file.py ClassName``

Resume Previous Render
----------------------

While rendering, PianoRay saves which frame is currently being rendered to
the cache. This allows resuming a render if it is interrupted.

Configure render resuming with the ``--resume=...`` flag.

- If omitted, PianoRay will ask via stdin if you wish to resume.
- If ``True``, PianoRay will always resume if a previous render exists.
- If ``False``, PianoRay will never resume.

If the previous render finished completely, you can pass ``--resume=True``
to only recompile the frames into a video.
