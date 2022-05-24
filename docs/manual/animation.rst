Animation
=========

Animation is done on :class:`pianoray.Property` with :class:`~pianoray.Keyframe`
instances. Each keyframe contains a frame, a value, and an interpolation.

Syntax
------

Call the ``animate`` method on :class:`pianoray.Property`:

.. code-block:: py

   def setup(self):
       # All syntaxes do the same thing.
       self.group.prop.animate(frame, value, interp)
       self.group.prop.animate((frame, value, interp))
       self.group.prop.animate(
           (frame, value, interp),
           (frame2, value2, interp2),
       )
       self.group.prop.animate(Keyframe(frame, value, interp))


