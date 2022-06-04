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

Example recordings and renders.

pianoray
--------

Source code for everything.

pianoray/
^^^^^^^^^

Main module and global utilities.
Entry point is here (``__main__``).

pianoray/cutils
^^^^^^^^^^^^^^^

C++ libraries for rendering.

pianoray/effects
^^^^^^^^^^^^^^^^

OOP effects for organization. Most call libraries from ``cutils``.

pianoray/render
^^^^^^^^^^^^^^^

Rendering pipeline.

pianoray/view
^^^^^^^^^^^^^

PianoRay viewer. Currently in development.

scripts
-------

Small scripts, like style checks.

tests
-----

Testing files, like test video settings.
