CLI
===

Driver CLI manual.

``usage: pianoray [-h] [-V] [-v] -p PATHS -o OUTPUT graph``

- ``-h``: Help
- ``-V``: Version
- ``-p``: Path(s) to kernels e.g. ``build/kernels``. Pass the folder
  containing the folders of kernels. Separate paths with ``":"``.
- ``-o``: Output video file.
- ``graph``: Pipeline file and class name e.g. ``/path/file.py:PipelineClass``

Example Commands
----------------

.. code-block:: sh

   # help
   pianoray --help

   # version
   pianoray --version

   # render pipeline
   # - paths of kernels: ./build/kernels
   # - output file: out.mp4
   # - python file containing pipeline: ./mozart.py
   # - python pipeline class name: RedBlocks
   pianoray -p ./build/kernels -o out.mp4 ./mozart.py:RedBlocks

   # - paths of kernels: ./build/kernels, /usr/share/pianoray/kernels
   #   notice the colon : separating the paths
   pianoray -p ./build/kernels:/usr/share/pianoray/kernels
