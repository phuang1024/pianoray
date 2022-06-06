C Integration
=============

Description of how C libraries are integrated with Python.

All C code is in ``pianoray/cutils``.

Code that calls the compiler is in ``pianoray/cpp.py``.

Compilation
-----------

At every run, the libraries are compiled and stored in the cache directory
(default ``.prcache``).

Loading
-------

Libraries are compiled to shared libraries (``.so``) and loaded with the
Python ``ctypes`` module.

Conventions
-----------

Images are of shape ``(height, width, 3)`` and type ``uint8`` and ``double``.
See :doc:`Rendering <./render>` for more info on how rendering is done.

Parsed MIDI notes (start, end, note, velocity) are serialized as a string
Python side and parsed C side in order to reduce the amount of function
arguments (one ``char*`` vs four ``double*``). Serialization specification
can be found in :doc:`Specifications <./specs>`.
