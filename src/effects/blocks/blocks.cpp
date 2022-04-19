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
 * Distance to a block.
 *
 * @param px, py  Point coordinates.
 * @param x, y, w, h, r  Block dimensions.
 */
double dist_to_block(double px, double py, double x, double y,
    double w, double h, double r)
{
    // Mirror across block center to simply calcs.
    double half_x = x + w/2;
    double half_y = y + h/2;
    if (px > half_x)
        px -= 2 * (px-half_x);
    if (py > half_y)
        py -= 2 * (py-half_y);

    // Center of rounding.
    double cx = x + r, cy = y + r;

    if (px < cx && py < cy)
        return hypot(cx-px, cy-py) - r;
    else if (px < x && py >= cy)
        return x - px;
    else if (px >= cx && py < y)
        return y - py;
    else
        return 0;
}


/**
 * Draw rectangle.
 *
 * @param width, height  Image dimensions.
 * @param x, y, w, h, r  Rectangle dimensions.
 */
void draw_rect(
    Image& img, int width, int height,
    double x, double y, double w, double h, double r)
{
    int x_min = (int)(dbounds(x-2, 0, width-1));
    int x_max = (int)(dbounds(x+w+3, 0, width-1));
    int y_min = (int)(dbounds(y-2, 0, height-1));
    int y_max = (int)(dbounds(y+h+3, 0, height-1));

    for (int px = x_min; px < x_max; px++) {
        for (int py = y_min; py < y_max; py++) {
            double dist = dist_to_block(px, py, x, y, w, h, r);
            double alpha = interp(dist, 0, 1.5, 1, 0);
            alpha = dbounds(alpha, 0, 1) * 255;

            for (int i = 0; i < 3; i++)
                img.set(px, py, i, alpha);
        }
    }
}


/**
 * Render blocks.
 *
 * @param num_notes  Number of MIDI notes passed in.
 * @param note_starts  Start frame of each note.
 * @param note_ends  End frame of each note.
 */
extern "C" void render_blocks(
    UCH* img_data, int width, int height,
    int num_notes, double* note_starts, double* note_ends)
{
    Image img(img_data, width, height, 3);
    draw_rect(img, width, height, 50, 50, 50, 100, 5);

    for (int note = 0; note < num_notes; note++) {
    }
}


}  // namespace Pianoray

