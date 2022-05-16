#include <iostream>

#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"


namespace Pianoray {


struct Rect {
    double x, y, w, h;
};


/**
 * Absolute distance to a block.
 *
 * @param px, py  Point coordinates.
 * @param r  Block rounding radius.
 */
double dist_to_block(double px, double py, const Rect& rect, double r)
{
    const double x = rect.x, y = rect.y, w = rect.w, h = rect.h;

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
 * Set block_fac and glow_fac values.
 *
 * @param width, height  Image dimensions.
 */
void set_fac(
    ImageGray& block_fac, ImageGray& glow_fac,
    const Rect& rect, double radius, double glow_radius, double glow_int)
{
    const double gr = glow_radius;
    const double x = rect.x, y = rect.y, w = rect.w, h = rect.h;
    const int width = block_fac.width, height = block_fac.height;

    int x_min = (int)(dbounds(x-gr-1, 0, width-1));
    int x_max = (int)(dbounds(x+w+gr+2, 0, width-1));
    int y_min = (int)(dbounds(y-gr-1, 0, height-1));
    int y_max = (int)(dbounds(y+h+gr+2, 0, height-1));

    for (int x = x_min; x < x_max; x++) {
        for (int y = y_min; y < y_max; y++) {
            double dist = dist_to_block(x, y, rect, radius);

            double bfac = interp(dist, 0, 1, 1, 0);
            bfac = dbounds(bfac, 0, 1);

            double gfac = interp(dist, 1, gr, 1, 0);
            gfac = dbounds(gfac, 0, 1);
            gfac *= glow_int;

            block_fac.set(x, y, std::max(bfac, block_fac.get(x, y)));
            glow_fac.set(x, y, std::max(gfac, glow_fac.get(x, y)));
        }
    }
}


/**
 * Draw the blocks based on block and glow factors.
 */
void draw_blocks(
    Image& img, const ImageGray& block_fac, const ImageGray& glow_fac,
    const Color& color, const Color& glow_color)
{
    for (int x = 0; x < img.width; x++) {
        for (int y = 0; y < img.height/2; y++) {
            double bfac = block_fac.get(x, y);
            double gfac = glow_fac.get(x, y);

            Color curr = img.getc(x, y);
            curr = mix_cols(curr, glow_color, gfac);
            curr = mix_cols(curr, color, bfac);
            img.setc(x, y, curr);
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
    ImageGray block_fac(width, height), glow_fac(width, height);
    Color color(color_data), glow_color(glow_color_data);

    for (int i = 0; i < num_notes; i++) {
        double y_start = event_coord(note_starts[i], frame, height, fps, speed);
        double y_end = event_coord(note_ends[i], frame, height, fps, speed);

        y_start = dbounds(y_start, -radius, height/2 + radius);
        y_end = dbounds(y_end, -radius, height/2 + radius);
        double y_up, y_down;  // Y bounds up and down.
        if (y_start < y_end) {
            y_up = y_start;
            y_down = y_end;
        } else {
            y_down = y_start;
            y_up = y_end;
        }
        if (y_down < 0 || y_up > height/2)
            continue;

        double x_start, x_end;
        key_coords(x_start, x_end, note_keys[i], width, black_width);

        Rect rect;
        rect.x = x_start;
        rect.y = y_up;
        rect.w = x_end - x_start;
        rect.h = y_down - y_up;

        set_fac(block_fac, glow_fac, rect, radius, glow_radius, glow_int);
    }

    draw_blocks(img, block_fac, glow_fac, color, glow_color);
}


}  // namespace Pianoray

