First Video
===========

First, install PianoRay. Follow instructions in
`General/Installation <../general/install.html>`__.

Example Files
-------------

Download example performance files. This script copies the Fur Elise example
recording to ``~/pianoray_tutorial``.

.. code-block:: bash

   cd /tmp
   git clone https://github.com/phuang1024/pianoray
   cd pianoray/examples/furelise

   mkdir ~/pianoray_tutorial
   cp video.mp4 midi.mid audio.mp3 ~/pianoray_tutorial

The video file contains the recording of the piano. The MIDI file contains
data about which notes are played. The audio file has the audio.

Create Settings
---------------

In order to convey settings to PianoRay, we use the Python API. The API usage
is described in detail in TODO.

Save this data to ``~/pianoray_tutorial/furelise.py``:

.. code-block:: py

   from pianoray import *

   class FurElise(DefaultScene):
       def setup(self):
           self.video.resolution = (960, 540)
           self.video.fps = 30

           self.midi.file = "examples/furelise/midi.mid"

           self.audio.file = "examples/furelise/audio.mp3"
           self.audio.start = 20.74

           self.keyboard.file = "examples/furelise/video.mp4"
           self.keyboard.start = 4.75
           self.keyboard.crop = ((252,480), (1793,487), (1789,676), (257,666))

This creates a new scene called ``FurElise`` with some settings.
PianoRay will read the scene to obtain settings.

Render
------

To start the render, run these commands in a shell:

.. code-block:: bash

   cd ~/pianoray_tutorial
   pianoray render furelise.py FurElise -p

This starts rendering, using the provided Python script and class name.
The ``-p`` flag tells PianoRay to open the output file after rendering.

Rendering may take a few minutes. If the renderer crashes, run the same command
again. If it repeatedly does not work, open an issue on GitHub for help.
