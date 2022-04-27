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

#include <cmath>
#include <cstring>
#include <fstream>
#include <iostream>

#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"
#include "pr_random.hpp"


namespace Pianoray {


/**
 * Render glare at one position.
 *
 * @param cached, cache  Cache data.
 * @param cx, cy  Glare center pixel coordinates.
 * @param streak_angles_uch  Angles for this glare's streaks.
 */
void render_one_glare(Image& img, int note, double cx, double cy,
    double radius, double intensity, double jitter, int streaks,
    UCH* streak_angles_uch)
{
    double streak_angles[20];
    for (int i = 0; i < streaks; i++)
        streak_angles[i] = ((double)streak_angles_uch[i]/128 - 0.5) * PI;

    const Color white(255, 255, 255);
    const double rand_mult = Random::uniform(1-jitter, 1+jitter);

    int w = img.width, h = img.height;

    int x_start = ibounds((int)(cx-radius), 0, w-1);
    int x_end = ibounds((int)(cx+radius+1), 0, w-1);
    int y_start = ibounds((int)(cy-radius), 0, h-1);
    int y_end = ibounds((int)(cy+radius+1), 0, h-1);

    for (int x = x_start; x <= x_end; x++) {
        for (int y = y_start; y <= y_end; y++) {
            // Compute factor from streaks.
            int dy = y - cy, dx = x - cx;
            double angle = atan2(dy, dx);
            double prox = 100;
            for (int i = 0; i < streaks; i++) {
                double dist = fabs(angle - streak_angles[i]);
                if (dist < prox)
                    prox = dist;
            }
            double fac_streak = dbounds(interp(prox, 0, 0.1, 1.1, 1), 1, 1.04);

            // Compute factor from radius.
            // Slightly increases radius if close to streak.
            int r = hypot(x-cx, y-cy);
            double real_rad = interp(fac_streak, 1, 1.1, radius, radius*1.1);
            double fac_rad = dbounds(1 - r/real_rad, 0, 1);
            fac_rad = pow(fac_rad, 2);  // Square falloff

            // Color pixel
            double fac = interp(fac_streak*fac_rad, 0, 1, 0, intensity);
            fac *= rand_mult;

            Color curr = img.getc(x, y);
            img.setc(x, y, mix_cols(curr, white, fac));
        }
    }
}


/**
 * Render glare.
 *
 * @param img_data, width, height  Image parameters.
 * @param frame  Frame to render.
 *
 * @param num_notes  Number of MIDI notes passed in.
 * @param note_keys  Key (note number) for each note.
 * @param note_starts  Start frame of each note.
 * @param note_ends  End frame of each note.
 * @param streak_angles  Angles, corresponding to each note. Each element of
 *     this array is another array of UCH length 20, containing the streak
 *     angles.
 *
 * @param black_width  settings.piano.black_width_fac
 * @param radius  settings.glare.radius
 * @param intensity  settings.glare.intensity
 * @param jitter  settings.glare.jitter
 * @param streaks  settings.glare.streaks
 */
extern "C" void render_glare(
    UCH* img_data, int width, int height,
    int frame,
    int num_notes, int* note_keys, double* note_starts, double* note_ends,
        UCH (*streak_angles)[20],
    double black_width, double radius, double intensity, double jitter,
        int streaks)
{
    Image img(img_data, width, height, 3);
    int half = height / 2;

    // Render
    for (int i = 0; i < num_notes; i++) {
        double start = note_starts[i];
        double end = note_ends[i];

        if (start < frame && frame < end) {
            int note = note_keys[i];
            double key_x = key_pos(note) * width;

            render_one_glare(img, note, key_x, half, radius,
                intensity, jitter, streaks, streak_angles[i]);
        }
    }
}


}  // namespace Pianoray
