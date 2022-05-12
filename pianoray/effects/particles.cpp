#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>

#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"


namespace Pianoray {


struct Particle {
    double x, y;
    double vx, vy;  // velocity in px/frame
    double life;  // duration in frames
};


/**
 * Read cache of particles.
 */
struct CacheRead {
    int length;
    std::vector<Particle> ptcls;

    CacheRead(char* path) {
        if (strlen(path) == 0) {
            length = 0;
        }
        else {
            std::ifstream fin(path);
            fin.read((char*)(&length), sizeof(int));
            for (int i = 0; i < length; i++) {
                Particle p;
                fin.read((char*)(&p), sizeof(Particle));
                ptcls.push_back(p);
            }
        }
    }
};

/**
 * Write particles.
 */
struct CacheWrite {
    int length;
    std::ofstream fout;

    ~CacheWrite() {
        fout.seekp(0, fout.beg);
        fout.write((char*)(&length), sizeof(int));
    }

    CacheWrite(char* path) {
        fout = std::ofstream(path);
        fout.seekp(sizeof(int), fout.beg);

        length = 0;
    }

    void write(const Particle& ptcl) {
        fout.write((char*)(&ptcl), sizeof(Particle));
        length++;
    }
};


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

    CacheRead cache_in(cache_in_path);
    Image img(img_data, width, height, 3);

    CacheWrite cache_out(cache_out_path);
    for (int i = 0; i < cache_in.length; i++)
        cache_out.write(cache_in.ptcls[i]);

    std::cerr << frame << ' ' << cache_in.length << ' ' << cache_out.length << std::endl;
    if (frame == 0) {
        Particle ptcl;
        cache_out.write(ptcl);
    }
}


}  // namespace Pianoray


/*
using namespace Pianoray;
int main() {
    CacheRead in("in.cache");
    CacheWrite out("out.cache");

    std::cerr << "in len: " << in.length << std::endl;

    std::cerr << "Copying in to out." << std::endl;
    for (int i = 0; i < in.length; i++)
        out.write(in.ptcls[i]);

    std::cerr << "Adding one." << std::endl;
    Particle ptcl;
    out.write(ptcl);

    std::cerr << "Done." << std::endl;
}*/
