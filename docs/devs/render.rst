Rendering Pipeline
==================

Description of how rendering is done internally.

First, an image of 64-bit floats is created. This is like an unbounded brightness
image of the rendered scene, and will be converted into a standard 8-bit int later.

Each effects is applied to the image.

Last, the compositing library processes the double image, such as adding glare.
After everything is finished, the float image is converted into an int image using
``tanh`` as the transformation function.
