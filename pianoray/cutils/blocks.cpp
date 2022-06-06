#include <iostream>

#include "pr_image.hpp"
#include "pr_midi.hpp"
#include "pr_piano.hpp"


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


void draw_block(ImageD& img, const Rect& rect, const ColorD& color, double radius,
        double bottom_glow, double bottom_glow_len) {
    const double x = rect.x, y = rect.y, w = rect.w, h = rect.h;
    const int width = img.width, height = img.height;
    const int half = height / 2;
    const bool playing = (y+h) >= half;

    int x_min = (int)dbounds(x-1, 0, width-1);
    int x_max = (int)dbounds(x+w+2, 0, width-1);
    int y_min = (int)dbounds(y-1, 0, half);
    int y_max = (int)dbounds(y+h+2, 0, half);

    for (int x = x_min; x < x_max; x++) {
        for (int y = y_min; y < y_max; y++) {
            double dist = dist_to_block(x, y, rect, radius);
            double fac = dbounds(interp(dist, 0, 1, 1, 0), 0, 1);

            if (playing && half-y <= bottom_glow_len) {
                double glow_fac = interp(half-y, 0, bottom_glow_len, 1, 0);
                double glow_mult = interp(pow(glow_fac, 2), 0, 1, 1, bottom_glow);
                img.overlay(x, y, color.mult(glow_mult), fac);
            } else {
                img.overlay(x, y, color, fac);
            }
        }
    }
}


/**
 * New render blocks.
 */
extern "C" void render_blocks(
    DImg d_img, int width, int height,
    int frame, char* notes_str,
    double p_video_fps, double p_piano_blackWidthFac, double p_blocks_speed,
    double* dp_blocks_color, double p_blocks_radius, double p_blocks_bottomGlow,
    double p_blocks_bottomGlowLen
) {
    ImageD img(d_img, width, height);
    Midi midi(notes_str);
    ColorD p_blocks_color(dp_blocks_color);

    for (int i = 0; i < midi.count; i++) {
        const Note note = midi[i];

        // Y bounds of rect.
        double y_start = event_coord(note.start, frame, height, p_video_fps,
            p_blocks_speed);
        double y_end = event_coord(note.end, frame, height, p_video_fps,
            p_blocks_speed);

        // Not sure of y_start, y_end order so check here.
        double y_up, y_down;
        if (y_start < y_end) {
            y_up = y_start;
            y_down = y_end;
        } else {
            y_down = y_start;
            y_up = y_end;
        }
        if (y_down < 0 || y_up > height/2)
            continue;

        // X bounds of note.
        double x_start, x_end;
        key_coords(x_start, x_end, note.note, width, p_piano_blackWidthFac);

        Rect rect;
        rect.x = x_start;
        rect.y = y_up;
        rect.w = x_end - x_start;
        rect.h = y_down - y_up;

        draw_block(img, rect, p_blocks_color, p_blocks_radius, p_blocks_bottomGlow,
            p_blocks_bottomGlowLen);
    }
}
