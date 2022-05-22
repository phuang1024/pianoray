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
void write_cache(const std::vector<Particle>& ptcls, const std::vector<bool>& good,
        char* path) {
    int length = ptcls.size();

    std::ofstream fout = std::ofstream(path);
    fout.write((char*)(&length), sizeof(int));

    for (int i = 0; i < length; i++)
        if (good[i])
            fout.write((char*)(&ptcls[i]), sizeof(Particle));
};


/**
 * Get vector of wind at coord.
 * Stores in param wx, wy.
 *
 * @param x, y  Coords.
 * @param t  Seconds.
 */
void wind(double& wx, double& wy, double x, double y, double t) {
    double v = (x+y)*2 + t;
    wx = cos(v);
    wy = sin(v);
}


void render(Image& img, int frame, const std::vector<Particle>& ptcls,
        const std::vector<bool>& good, double lifetime) {
    const double rad = img.width / 750.0;  // Radius of ptcl at max strength

    ImageGray factor(img.width, img.height);

    for (const Particle& ptcl: ptcls) {
        double strength = (double)(frame-ptcl.birth) / lifetime;
        strength = 1 - pow(strength, 2);
        if (strength <= 0)
            continue;

        double r = rad * strength;  // decrease rad
        int x_min = ibounds(ptcl.x-r, 0, img.width-1);
        int x_max = ibounds(ptcl.x+r+1, 0, img.width-1);
        int y_min = ibounds(ptcl.y-r, 0, img.height-1);
        int y_max = ibounds(ptcl.y+r+1, 0, img.height-1);

        for (int x = x_min; x <= x_max; x++) {
            for (int y = y_min; y <= y_max; y++) {
                double dist = hypot(x-ptcl.x, y-ptcl.y);
                double fac = dbounds(interp(dist, 0, r, strength, 0), 0, strength);
                factor.set(x, y, std::max(factor.get(x, y), fac));
            }
        }
    }

    const Color white(255, 255, 255);
    for (int x = 0; x < img.width; x++) {
        for (int y = 0; y < img.height; y++) {
            Color curr = img.getc(x, y);
            Color mix = mix_cols(curr, white, factor.get(x, y));
            img.setc(x, y, mix);
        }
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
 *
 * @param fps  props.video.fps
 * @param pps  props.ptcls.pps
 * @param air_resist  props.ptcls.air_resist
 * @param lifetime  props.ptcls.lifetime
 * @param x_vel  props.ptcls.x_vel
 * @param y_vel  props.ptcls.y_vel
 * @param wind_str  props.ptcls.wind_strength
 * @param heat_str  props.ptcls.heat_strength
 */
extern "C" void render_ptcls(
    UCH* img_data, int width, int height,
    int frame,
    char* cache_in_path, char* cache_out_path,
    int num_notes, int* note_keys, double* note_starts, double* note_ends,
    int fps, double pps, double air_resist, double lifetime, double x_vel,
        double y_vel, double wind_str, double heat_str, double gravity)
{
    const double ppf = pps / fps;
    air_resist = pow(air_resist, 1.0 / fps);
    lifetime *= fps;
    wind_str /= fps;
    heat_str /= fps / 2;
    gravity /= fps;

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
                double vx = Random::uniform(-x_vel, x_vel);
                double vy = Random::uniform(-y_vel, -y_vel/2);
                ptcls.push_back(Particle(key_x, height/2, vx, vy, frame));
            }
        }
    }

    // Update s and v
    const double px_to_coord = 52.0 / width;
    for (Particle& ptcl: ptcls) {
        // s = integral(v), air resistance, gravity
        ptcl.x += ptcl.vx;
        ptcl.y += ptcl.vy;
        ptcl.vx *= air_resist;
        ptcl.vy *= air_resist;
        ptcl.vy += gravity;

        // Wind
        double wx, wy;
        wind(wx, wy, ptcl.x*px_to_coord, ptcl.y*px_to_coord, (double)(frame)/fps);
        wx *= wind_str;
        wy *= wind_str;
        ptcl.vx += wx;
        ptcl.vy += wy;

        // Heat rising
        double heat = 1 - (double)(frame-ptcl.birth) / lifetime;
        ptcl.vy -= heat * heat_str;  // minus bc up is minus
    }

    std::vector<bool> good;  // ptcls to carry to next frame
    for (Particle ptcl: ptcls) {
        bool g = true;
        if (
            ptcl.x < 0 || ptcl.x >= width ||
            ptcl.y < 0 || ptcl.y >= height ||
            frame - ptcl.birth > lifetime
        )
            g = false;

        good.push_back(g);
    }

    render(img, frame, ptcls, good, lifetime);
    write_cache(ptcls, good, cache_out_path);
}


}  // namespace Pianoray
