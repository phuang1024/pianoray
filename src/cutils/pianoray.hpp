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


}  // namespace Pianoray
