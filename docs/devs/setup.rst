Setup
=====

How to setup your development environment.

Fork and Clone
--------------

First, fork the GitHub repository and clone your fork.

Dependencies
------------

- Python3.8 or above
- Make
- FFmpeg

Python packages: Install from ``requirements.txt``:
``pip install -r requirements.txt``

Test Video
----------

.. code-block:: bash

   cd /path/to/pianoray
   make wheel
   make install
   pianoray -s tests/settings.json -o out.mp4 -p
