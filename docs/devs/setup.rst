Setup
=====

How to setup your development environment.

Dependencies
------------

See dependencies in :doc:`../general/install`.

Additional dependencies for development:

- Git
- GNU Make

Fork and Clone
--------------

First, fork the GitHub repository and clone your fork.

Test Video
----------

.. code-block:: bash

   cd /path/to/pianoray
   make wheel
   make install
   pianoray render tests/furelise.py FurElise -o out.mp4 -p

This should render the video and open it in your video player. Rendering
may take a few minutes.
