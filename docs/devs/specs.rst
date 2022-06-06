Specifications
==============

Specs of internally used protocols.

MIDI Notes
----------

Notes are parsed from a MIDI file using the Python module ``mido``. In order
to simplify passing these notes to C functions, we serialize them into a string
Python side and parse them C side. This reduces the amount of arguments required
for a C function and removes boilerplate code.

Each note is stored internally as four values, ``(start_frame, end_frame, note,
velocity)``. The serialized string representing a sequence of notes is as follows:

.. code-block:: text

   uint32 (4bytes): How many notes there are.
   For each note:
       double (8bytes): Start frame.
       double (8bytes): End frame.
       uint8 (1byte): Note index.
       uint8 (1byte): Velocity.
