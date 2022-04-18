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

#include <algorithm>


namespace Pianoray {


typedef  unsigned char  UCH;


class Image {
public:
    UCH* data;
    int width, height, channels;

    /**
     * Initialize.
     * @param data  Memory of values.
     *              Shape should be (height, width, channel)
     */
    Image(UCH* data, int width, int height, int channels) {
        this->data = data;
        this->width = width;
        this->height = height;
        this->channels = channels;
    }

    /**
     * Index of data for corresponding coords.
     */
    int index(int x, int y, int ch) {
        return (
            y * width * channels +
            x * channels +
            ch
        );
    }

    /**
     * Get value at coord.
     */
    UCH get(int x, int y, int ch) {
        return data[index(x, y, ch)];
    }

    /**
     * Set value at coord.
     */
    void set(int x, int y, int ch, UCH v) {
        data[index(x, y, ch)] = v;
    }
};


double hypot(double x, double y) {
    return pow(x*x + y*y, 0.5);
}

int ibounds(int v, int min, int max) {
    return std::min(std::max(v, min), max);
}

double dbounds(double v, double min, double max) {
    return std::min(std::max(v, min), max);
}


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
    double white_width = 1 / 52;

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




/*
def key_coords(settings: Settings, key: int) -> Tuple[float, float]:
    """
    Horizontal (x) coordinates of key on the screen.
    :param key: Key.
    :return: ``(start_coord, end_coord)`` of key.
    """
    center = np.interp(key_pos(key), (0, 1), (0, settings.video.resolution[0]))
    white_width = settings.video.resolution[0] / 52
    black_width = white_width * settings.piano.black_width_fac
    width = white_width if is_white_key(key) else black_width
    half = width / 2
    return (center-half, center+half)


def note_coords(settings: Settings, event_frame: float,
        frame: float) -> float:
    """
    Vertical (y) coordinates of an event as it is dropping from the top
    to the keyboard.
    :param event_frame: The time of the event.
    :param frame: Current frame.
    :return: Y pixel position.
    """
    height = settings.video.resolution[1] / 2
    speed = (settings.blocks.speed * height / settings.video.fps)
    delta = speed * (frame-event_frame)
    return height + delta
*/


}  // namespace Pianoray
