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

#include "pr_math.hpp"


namespace Pianoray {


typedef  unsigned char  UCH;


/**
 * RGB color.
 */
struct Color {
    UCH r, g, b;

    /**
     * Initialize all 0.
     */
    Color() {
        r = g = b = 0;
    }

    /**
     * Initialize with given values.
     */
    Color(UCH r, UCH g, UCH b) {
        this->r = r;
        this->g = g;
        this->b = b;
    }

    /**
     * Initialize from rgb data.
     */
    Color(UCH* data) {
        r = data[0];
        g = data[1];
        b = data[2];
    }
};


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
     * Get value as a color.
     */
    Color getc(int x, int y) {
        int i = index(x, y, 0);
        return Color(data[i], data[i+1], data[i+2]);
    }

    /**
     * Set value at coord.
     */
    void set(int x, int y, int ch, UCH v) {
        data[index(x, y, ch)] = v;
    }

    /**
     * Set value to color.
     */
    void setc(int x, int y, const Color& c) {
        int i = index(x, y, 0);
        data[i] = c.r;
        data[i+1] = c.g;
        data[i+2] = c.b;
    }
};


/**
 * Mix colors.
 * @param fac  Factor of mix from 0 to 1. 0 means all c1. 1 means all c2.
 */
Color mix_cols(const Color& c1, const Color& c2, double fac) {
    double fac1 = 1 - fac;
    double fac2 = fac;
    UCH r = ibounds(c1.r*fac1 + c2.r*fac2, 0, 255);
    UCH g = ibounds(c1.g*fac1 + c2.g*fac2, 0, 255);
    UCH b = ibounds(c1.b*fac1 + c2.b*fac2, 0, 255);
    return Color(r, g, b);
}


}  // namespace Pianoray
