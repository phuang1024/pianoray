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
    double x, double y, double w, double h, double r,
    const Color& color, double glow_int, double glow_radius,
    const Color& glow_color)
{
    double gr = glow_radius;
    int x_min = (int)(dbounds(x-gr-1, 0, width-1));
    int x_max = (int)(dbounds(x+w+gr+2, 0, width-1));
    int y_min = (int)(dbounds(y-gr-1, 0, height-1));
    int y_max = (int)(dbounds(y+h+gr+2, 0, height-1));

    for (int px = x_min; px < x_max; px++) {
        for (int py = y_min; py < y_max; py++) {
            double dist = dist_to_block(px, py, x, y, w, h, r);
            const Color curr = img.getc(px, py);

            double block_fac = interp(dist, 0, 1, 1, 0);
            block_fac = dbounds(block_fac, 0, 1);

            double glow_fac = interp(dist, 1, gr, 1, 0);
            glow_fac = dbounds(glow_fac, 0, 1);
            //glow_fac = pow(dbounds(glow_fac, 0, 1), 2);
            glow_fac *= glow_int;

            Color with_glow = mix_cols(curr, glow_color, glow_fac);
            Color with_block = mix_cols(with_glow, color, block_fac);
            img.setc(px, py, with_block);
        }
    }
}


/**
 * Render blocks.
 *
 * @param img_data, width, height  Image parameters.
 * @param frame  Frame to render.
 *
 * @param num_notes  Number of MIDI notes passed in.
 * @param note_keys  Key (note number) for each note.
 * @param note_starts  Start frame of each note.
 * @param note_ends  End frame of each note.
 *
 * @param fps  settings.video.fps
 * @param speed  settings.blocks.speed
 * @param black_width  settings.piano.black_width_fac
 * @param radius  settings.blocks.radius
 * @param color_data  settings.blocks.color
 * @param glow_int  settings.blocks.glow_intensity
 * @param glow_color_data  settings.blocks.glow_color
 */
extern "C" void render_blocks(
    UCH* img_data, int width, int height,
    int frame,
    int num_notes, int* note_keys, double* note_starts, double* note_ends,
    int fps, double speed, double black_width, double radius, UCH* color_data,
        double glow_int, double glow_radius, UCH* glow_color_data)
{
    Image img(img_data, width, height, 3);
    Color color(color_data), glow_color(glow_color_data);

    for (int i = 0; i < num_notes; i++) {
        double y_start = event_coord(note_starts[i], frame, height, fps, speed);
        double y_end = event_coord(note_ends[i], frame, height, fps, speed);
        if (y_start < 0 || y_end > height/2)
            continue;

        y_start = dbounds(y_start, -radius, height/2 + radius);
        y_end = dbounds(y_end, -radius, height/2 + radius);
        double x_start, x_end;
        key_coords(x_start, x_end, note_keys[i], width, black_width);

        double x = x_start;
        double y = y_end;
        double w = x_end - x_start;
        double h = y_start - y_end;
        draw_rect(img, width, height, x, y, w, h, radius, color,
            glow_int, glow_radius, glow_color);
    }
}


}  // namespace Pianoray

