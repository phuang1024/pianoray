Tutorial
========

First, install PianoRay. Follow instructions in General/Installation.

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

PianoRay reads settings from a JSON file. This file contains nested mappings
with ``key: value`` pairs.

Save this data to ``~/pianoray_tutorial/settings.json``:

.. code-block:: bash

   {
       "video": {
           "resolution": [1280, 720],
           "fps": 30
       },
       "midi": {
           "file": "midi.mid"
       },
       "audio": {
           "file": "audio.mp3",
           "start": 20.74
       },
       "keyboard": {
           "file": "video.mp4",
           "start": 4.75,
           "crop": [[252,480], [1793,487], [1789,676], [257,666]],
           "dim_mult": 0.6,
           "dim_add": -8
       }
   }

Most of these settings are self explanatory.

The ``start`` settings are timestamps, in seconds, of when you press the first
note in the respective media. This is necessary to apply the correct offsets.

The ``crop`` setting defines the coordinates of the keyboard in the video.
These values are for the Fur Elise recording.

Render
------

To start the render, run these commands in a shell:

.. code-block:: bash

   cd ~/pianoray_tutorial
   pianoray -s settings.json -o out.mp4 -p

This starts rendering, using the provided settings file and saving to the
output file. The ``-p`` flag tells PianoRay to open the output file after
rendering.

Rendering may take a few minutes.
