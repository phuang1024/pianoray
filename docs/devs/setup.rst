Setup
=====

How to setup your development environment.

Fork and Clone
--------------

First, fork the GitHub repository and clone your fork.

Dependencies
------------

See dependencies in the ``General/Installation`` page.

Additional dependencies for development:

- Git
- GNU Make


Test Video
----------

.. code-block:: bash

   cd /path/to/pianoray
   make wheel
   make install
   pianoray -s tests/furelise.json -o out.mp4 -p

This should render the video and open it in your video player. Rendering
may take a few minutes.
