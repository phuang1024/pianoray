#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>

#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"
#include "pr_random.hpp"


namespace Pianoray {


struct Particle {
    double x, y;
    double vx, vy;  // velocity in px/frame
    double birth;  // birth timestamp in frames

    Particle() {
        x = y = vx = vy = birth = 0;
    }

    Particle(double x, double y, double vx, double vy, double birth) {
        this->x = x;
        this->y = y;
        this->vx = vx;
        this->vy = vy;
        this->birth = birth;
    }
};


/**
 * Read cache of particles.
 */
void read_cache(std::vector<Particle>& ptcls, char* path) {
    if (strlen(path) > 0) {
        std::ifstream fin(path);
        int length;
        fin.read((char*)(&length), sizeof(int));

        for (int i = 0; i < length; i++) {
            Particle p;
            fin.read((char*)(&p), sizeof(Particle));
            ptcls.push_back(p);
        }
    }
}

/**
 * Write particles.
 */
void write_cache(std::vector<Particle>& ptcls, char* path) {
    int length = ptcls.size();

    std::ofstream fout = std::ofstream(path);
    fout.write((char*)(&length), sizeof(int));

    for (int i = 0; i < length; i++)
        fout.write((char*)(&ptcls[i]), sizeof(Particle));
};


void render_ptcls(Image& img, const std::vector<Particle>& ptcls) {
    const Color white(255, 255, 255);
    for (const Particle& ptcl: ptcls) {
        img.setc(ptcl.x, ptcl.y, white);
    }
}


/**
 * Render and simulate particles.
 *
 * @param img_data, width, height  Image parameters.
 * @param frame  Frame to render.
 *
 * @param num_notes  Number of MIDI notes passed in.
 * @param note_keys  Key (note number) for each note.
 * @param note_starts  Start frame of each note.
 * @param note_ends  End frame of each note.
 */
extern "C" void render_ptcls(
    UCH* img_data, int width, int height,
    int frame,
    char* cache_in_path, char* cache_out_path,
    int num_notes, int* note_keys, double* note_starts, double* note_ends,
    int fps, double pps)
{
    const double ppf = pps / fps;

    Image img(img_data, width, height, 3);

    std::vector<Particle> ptcls;
    read_cache(ptcls, cache_in_path);

    // Generate new ptcls
    for (int i = 0; i < num_notes; i++) {
        double start = note_starts[i];
        double end = note_ends[i];

        if (start < frame && frame < end) {
            int note = note_keys[i];
            double key_x = key_pos(note) * width;

            int num_ptcls = ppf * Random::uniform(0.5, 2);
            for (int j = 0; j < num_ptcls; j++) {
                ptcls.push_back(Particle(key_x, height/2, Random::uniform(-1, 1),
                    Random::uniform(-1, 0), frame));
            }
        }
    }

    render_ptcls(img, ptcls);

    write_cache(ptcls, cache_out_path);
}


}  // namespace Pianoray
