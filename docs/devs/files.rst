File Structure
==============

Information about the project files.

/
---

Root directory. Contains cool files.

Python module ``setup.py`` and ``MANIFEST.in`` are here.

There is a Makefile with convenient targets.

.github
-------

GitHub files, like workflows.

docs
----

Documentation. Docs are generated with Python sphinx and hosted on
ReadTheDocs.

examples
--------

Example recordings for testing.

pianoray
--------

Source code for everything.

pianoray/
^^^^^^^^^

Main module and global utilities.

- ``__init__.py``: Module file.
- ``cpp.py``: Handles C++ library compiling and loading.
- ``logger.py``: Logging utilities.
- ``main.py``: Main entry point.
- ``settings.py``: Class for convenient settings access.
- ``utils.py``: Global utilities.

pianoray/cutils
^^^^^^^^^^^^^^^

C++ header files for C++ libraries.

- ``pr_image.hpp``: Image class for interacting with raw unsigned char data.
- ``pr_math.hpp``: Math utilities.
- ``pr_piano.hpp``: Utilities relating to rendering, e.g. piano dimensions.
- ``pr_random.hpp``: Random number generator utilities.

pianoray/effects
^^^^^^^^^^^^^^^^

Files that render the video.

- ``effect.py``: Effect base class for OOP internally.
- ``midi.py``: Parse MIDI.
- ``blocks.py``, ``blocks.cpp``: Rendering blocks.
- ``glare.py``, ``glare.cpp``: Rendering glare.
- ``keyboard.py``: Rendering keyboard.

pianoray/render
^^^^^^^^^^^^^^^

Rendering pipeline.

- ``render.py``: Calling effects to render the video.
- ``video.py``: Class for managing video frames and calling FFmpeg to compile
  the video.
- ``lib.py``: Load and initialize C++ libraries.

pianoray/view
^^^^^^^^^^^^^

PianoRay viewer files. Currently in development.

scripts
-------

Small scripts, like style checks.

tests
-----

Testing files, like test JSON settings.
