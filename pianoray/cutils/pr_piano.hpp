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

#pragma once


namespace Pianoray {


/**
 * If key is white.
 */
bool is_white_key(int key) {
    int v = key % 12;
    if (v == 1 || v == 4 || v == 6 || v == 9 || v == 11)
        return false;
    return true;
}

/**
 * Position of the center of the key on the keyboard.
 * @return  Factor from 0 to 1 (start of first key to end of last).
 */
double key_pos(int key) {
    double white_width = 1.0 / 52;

    bool last_white = false;  // Last key is white
    double pos = 0;
    for (int k = 0; k <= key; k++) {
        bool white = is_white_key(k);
        if (white && last_white)
            pos += white_width;
        else
            pos += white_width / 2;
        last_white = white;
    }

    return pos;
}


/**
 * Horizontal X coordinates of the left and right ends of a key.
 *
 * @param left, right  References which will be modified to contain the returns.
 * @param key  Key number.
 * @param width  settings.video.resolution[0]
 * @param black_width_fac  settings.piano.black_width_fac
 */
void key_coords(
    double& left, double& right, int key,
    int width, double black_width_fac)
{
    double center = interp(key_pos(key), 0, 1, 0, width);
    double white_width = width / 52;
    double key_width = is_white_key(key) ? white_width :
        white_width * black_width_fac;
    double half = key_width / 2;

    left = center - half;
    right = center + half;
}

/**
 * Vertical Y coordinates of a MIDI event as it is dropping from the top
 * to the keyboard.
 *
 * @param event_frame  Frame the event happens.
 * @param frame  Current frame.
 * @param height  settings.video.resolution[1]
 * @param fps  settings.video.fps
 * @param speed  settings.blocks.speed
 */
double event_coord(
    double event_frame, double frame,
    int height, int fps, double speed)
{
    height /= 2;  // Piano takes up half of screen.
    speed *= height / fps;  // Convert to pixels per frame.
    double delta = speed * (frame-event_frame);
    return height + delta;
}


}  // namespace Pianoray
