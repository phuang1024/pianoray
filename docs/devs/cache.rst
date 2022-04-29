Cache
=====

PianoRay stores temporary files in a cache directory (default ``.prcache``).
The cache can be safely deleted at any time.

File Structure
--------------

- ``./c_libs``: Compiled C library object and library files.
- ``./output``: Output render is stored here.
- ``./settings.json``, ``./currently_rendering.txt``: Files that store the state
  of the rendering. This is used to resume rendering if desired. See
  `CLI <../manual/cli.html>`__ for more info.
