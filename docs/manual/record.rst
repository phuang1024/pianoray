Recording
=========

Instructions for recording and making your own video.

Recording
---------

You will need to record two files: Video and MIDI. In order to record these
files, you will need a MIDI keyboard, a camera, and a computer.

Video
^^^^^

Find a setup with a camera looking down vertically onto the keyboard.
Some things to consider:

- Safety: Make sure the camera won't fall down.
- Stability: Try to reduce shaking, e.g. from vibrations from the keyboard.
- Focus: Make sure you focus the camera onto the keyboard before recording.
  It is very disappointing to find that the video is ruined because the
  keyboard recording is blurry (speaking from experience).
- Background: If you desire, place a dark tarp under the keyboard so you can
  create the "hands floating over nothing" effect. There are some settings
  in PianoRay to dim the background and achieve this effect.
- Privacy: If you plan to release the video to the public, make sure it
  doesn't contain any private information.

MIDI
^^^^

Connect the MIDI keyboard to the computer. Use MIDI recording software to record
the MIDI. I use `MidiEditor <https://midieditor.org/>`__, which has worked great.

Processing
----------

Audio
^^^^^

Create an audio file from the MIDI.

1. Download a soundfont.
   `SoundFonts4U <https://sites.google.com/site/soundfonts4u>`__ has great piano
   soundfonts.
2. Install software that can render a MIDI file. I use
   `FluidSynth <https://github.com/FluidSynth/fluidsynth>`__, and the rest of
   these instructions assume you have FluidSynth.
3. Run this command, which uses FluidSynth to render and FFmpeg to write the audio
   file: ``fluidsynth -a alsa -T raw -g GAIN -F - SOUNDFONT.sf2 MIDI.mid |
   ffmpeg -y -f s32le -i - -filter:a "volume=2" AUDIO.mp3``. Replace the uppercase
   words with the respective values. A value of ``0.5`` for GAIN works usually.

Video
^^^^^

Make sure the video is right side up. That is, your hands come from the bottom of
the screen and play the keyboard.

If you need to rotate it, see
`this page <https://stackoverflow.com/a/9570992/16570071>`__ for rotating with FFmpeg.

Offsets
-------

Find the offsets for respective media. PianoRay uses these offsets. It may be
beneficial to write down these offsets somewhere so you don't forget them later.

Audio
^^^^^

Open the audio in an audio player and find the timestamp, in seconds, when the
audio starts. I use `Audacity <https://audacityteam.org>`__.

Video
^^^^^

Find the moment you play the first note in the video. I use
`Blender <https://blender.org>`__'s video editor.

Video Crop
^^^^^^^^^^

Find the pixel coordinates of the four corners of the keyboard in the video, starting
from the top left and going clockwise. If you use Blender's video editor, keep in mind
that Blender's image viewer has the Y coordinates reversed.

Rendering
---------

Follow instructions in `this page <first.html>`__ for rendering instructions.
