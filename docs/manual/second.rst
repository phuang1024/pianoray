Second Video
============

In this section, we will explore the API further.

Please follow the steps in :doc:`first` first, as we will use the setup
and code as a starting point.

Basics
------

The ``Scene`` class extends :class:`~pianoray.DefaultScene`, which is
defined internally. This scene contains :class:`~pianoray.PropertyGroup`
instances, each with their own :class:`~pianoray.Property`.

When we run code like ``self.video.resolution = ...``, we are setting
the value of the property. The available properties are documented in
:doc:`props`. The current properties we have changed are either not
exciting or mandatory.

Let's change the appearance of the video.

Changing Props
--------------

There is an available property ``blocks.color``, which allows us to set
the RGB color of the blocks.

Add this line somewhere in the ``setup`` method:

.. code-block:: py

   self.blocks.color = (255, 160, 160)  # Red

This will set the blocks to red. Run the render command to re-render the
video:

.. code-block:: sh

   pianoray render furelise.py FurElise -o out.mp4 -p

You may be asked whether you want to overwrite the output file. Choose yes.
The new video will have red blocks.

Animation
---------

In addition to setting values, the API also supports animating them. This
is done with keyframes.

Essentially, a keyframe contains a frame, a value, and an interpolation.
The frame is which frame the keyframe is. The value is the value at the
frame. The interpolation is how to transition from this keyframe to the
next. This is described in detail in :doc:`animation`.

.. warning::

   If a property is animated, PianoRay will ignore it's non-animated value:

   .. code-block:: py

      # This value will be used if there is no animation.
      self.blocks.color = ...

      # The animation will be used, but the value from the previous line
      # will be ignored.
      self.blocks.color.animate(...)

Animation is done with a property's ``animate`` method. Let's animate the
blocks changing from green to blue. Add these lines somewhere:

.. code-block:: py

   self.blocks.color.animate(
       (100, (160, 255, 160), Interp.LINEAR),  # Green
       (150, (160, 160, 255), Interp.LINEAR),  # Blue
    )

Render the video again and you should see the blocks change color somewhere
in the middle. Notice how the blocks are not red, even though the line above
sets them to red. Read the warning above to learn why.
