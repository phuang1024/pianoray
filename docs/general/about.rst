About
=====

PianoRay is software for piano visualization. The software can be categorized
into two parts:

- Driver: This is a Python program that exposes an API. Users define a pipeline
  with this api to decide how the rendering of each frame is processed.
- Kernels: The kernels are modules for computation. For example, one kernel
  processes MIDI data, another renders the glare, another the smoke, and so on.
  The kernels can be written in Python, Java, or C++ and are called by the
  driver based on the user's pipeline.
