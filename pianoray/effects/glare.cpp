//
//  PianoRay
//  Piano performance visualizer.
//  Copyright  PianoRay Authors  2022
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"


namespace Pianoray {


/**
 * Render glare.
 *
 * @param img_data, width, height  Image parameters.
 * @param frame  Frame to render.
 * @param num_notes  Number of MIDI notes passed in.
 * @param note_keys  Key (note number) for each note.
 * @param note_starts  Start frame of each note.
 * @param note_ends  End frame of each note.
 * @param fps  settings.video.fps
 * @param black_width  settings.piano.black_width_fac
 */
extern "C" void render_glare(
    UCH* img_data, int width, int height,
    int frame,
    int num_notes, int* note_keys, double* note_starts, double* note_ends,
    double black_width)
{
    Image img(img_data, width, height, 3);
    int half = height / 2;

    for (int i = 0; i < num_notes; i++) {
        double start = note_starts[i];
        double end = note_ends[i];

        if (start < frame && frame < end) {
            double x_start, x_end;
            key_coords(x_start, x_end, note_keys[i], width, black_width);

            for (int x = x_start; x < x_end; x++)
                for (int y = half-10; y < half+10; y++)
                    img.set(x, y, 0, 255);
        }
    }
}


}  // namespace Pianoray

