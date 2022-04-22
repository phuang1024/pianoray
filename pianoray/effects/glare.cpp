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
 * Stores information for one cached note.
 */
struct NoteCache {
    char note;
    char num_streaks;  // Number of streaks.
    char streaks[50];  // Streak angles, 256 units per revolution.
};


/**
 * Cache for glare.
 */
class Cache {
public:
    NoteCache notes[88];
    bool cached[88];    // Whether a note is cached.
    bool rendered[88];  // Whether a note is rendered in this frame.

    Cache() {
        memset(cached, 0, 88);
        memset(rendered, 0, 88);
    }

    void read(std::ifstream& fin) {
        memset(cached, 0, 88);
        memset(rendered, 0, 88);

        int count;
        fin.read((char*)(&count), sizeof(int));

        for (int i = 0; i < count; i++) {
            NoteCache c;
            fin.read((char*)(&c), sizeof(NoteCache));

            int note = c.note;
            cached[note] = true;
            notes[note] = c;
        }
    }

    void write(std::ofstream& fout) {
        int count = 0;
        for (int i = 0; i < 88; i++) {
            if (cached[i] && rendered[i]) {
                fout.write((char*)(&notes[i]), sizeof(NoteCache));
                count++;
            }
        }

        fout.seekp(0, std::ios::beg);
        fout.write((char*)(&count), sizeof(int));
    }
};


/**
 * Render glare at one position.
 *
 * @param cached, cache  Cache data.
 * @param cx, cy  Glare center pixel coordinates.
 */
void render_one_glare(Image& img, Cache& cache, int note,
    double cx, double cy, double radius, double intensity, double jitter,
    int streaks)
{
    const Color white(255, 255, 255);
    const double rand_mult = Random::uniform(1-jitter, 1+jitter);

    int w = img.width, h = img.height;

    int x_start = ibounds((int)(cx-radius), 0, w-1);
    int x_end = ibounds((int)(cx+radius+1), 0, w-1);
    int y_start = ibounds((int)(cy-radius), 0, h-1);
    int y_end = ibounds((int)(cy+radius+1), 0, h-1);

    // TODO render streaks
    for (int x = x_start; x <= x_end; x++) {
        for (int y = y_start; y <= y_end; y++) {
            int r = hypot(x-cx, y-cy);
            double fac = dbounds(1 - r/radius, 0, 1);
            fac = interp(fac, 0, 1, 0, intensity);
            fac *= rand_mult;
            fac = pow(fac, 2);  // Square falloff

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
 *
 * @param black_width  settings.piano.black_width_fac
 * @param radius  settings.glare.radius
 * @param intensity  settings.glare.intensity
 * @param jitter  settings.glare.jitter
 * @param jitter  settings.glare.streaks
 */
extern "C" void render_glare(
    UCH* img_data, int width, int height,
    int frame,
    char* cache_in_path, char* cache_out_path,
    int num_notes, int* note_keys, double* note_starts, double* note_ends,
    double black_width, double radius, double intensity, double jitter,
        const int streaks)
{
    Image img(img_data, width, height, 3);
    Cache cache;
    int half = height / 2;

    // Read cache
    if (strlen(cache_in_path) > 0) {
        std::ifstream fin(cache_in_path);
        cache.read(fin);
    }

    // Render
    for (int i = 0; i < num_notes; i++) {
        double start = note_starts[i];
        double end = note_ends[i];

        if (start < frame && frame < end) {
            int note = note_keys[i];
            double key_x = key_pos(note) * width;

            // Create cache entry if not already there.
            cache.rendered[note] = true;
            if (!cache.cached[note]) {
                cache.cached[note] = true;

                NoteCache& c = cache.notes[note];
                c.note = note;
                c.num_streaks = streaks;
                for (int i = 0; i < streaks; i++)
                    c.streaks[i] = Random::randint(0, 256);
            }

            render_one_glare(img, cache, note, key_x, half, radius,
                intensity, jitter, streaks);
        }
    }

    // Write cache
    if (strlen(cache_out_path) > 0) {
        std::ofstream fout(cache_out_path);
        cache.write(fout);
    }
}


}  // namespace Pianoray

