#include <iostream>

#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"


namespace Pianoray {


/**
 * Render and simulate particles.
 *
 * @param img_data, width, height  Image parameters.
 * @param frame  Frame to render.
 *
 * @param num_notes  Number of MIDI notes passed in.
 * @param note_keys  Key (note number) for each note.
 * @param note_starts  Start frame of each note.
 * @param note_ends  End frame of each note.
 */
extern "C" void render_ptcls(
    UCH* img_data, int width, int height,
    int frame,
    int num_notes, int* note_keys, double* note_starts, double* note_ends)
{
    Image img(img_data, width, height, 3);
}


}  // namespace Pianoray

