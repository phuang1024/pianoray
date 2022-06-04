Conventions
===========

Conventions used internally.

- Frame zero is when the first note begins.
- Note zero is lowest note on piano.
- One ``coord`` (unit of distance) is the width of one white key in the video.
  This is equal to the horizontal resolution divided by 52. For example, for a
  1920x1080 video, one coord is ``36.924`` pixels.
- C++ functions called by Python may take many arguments in order to obtain all
  required prop values. The naming convention is ``p_video_fps`` or ``d_img``
  or ``dp_blocks_color``. ``p`` means a property. ``d`` means raw data (numpy
  array pointer) which will be wrapped with an internal class.
