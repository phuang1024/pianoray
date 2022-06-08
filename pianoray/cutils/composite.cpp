#include <cmath>

#include "pr_image.hpp"


/**
 * Convert double image to char image using tanh.
 */
void double_to_char(ImageD& input, ImageC& output, double shutter) {
    for (int x = 0; x < input.width; x++) {
        for (int y = 0; y < input.height; y++) {
            ColorD raw = input.get(x, y);
            ColorC col;
            for (int i = 0; i < 3; i++) {
                double v = tanh(shutter * raw.get(i));
                col.set(i, 255 * v);
            }
            output.set(x, y, col);
        }
    }
}


void add_bloom(ImageD& img, double intensity, double radius, double thres) {
    // Will be added to original image.
    ImageD bloom(img.width, img.height);

    for (int x = 0; x < img.width; x++) {
        for (int y = 0; y < img.height/2; y++) {
            const ColorD col = img.get(x, y);
            double mag = (col.r+col.g+col.b) / 3.0;
            if (!(mag > 0 && mag >= thres))
                continue;

            for (int dx = -radius; dx <= radius+1; dx++) {
                for (int dy = -radius; dy <= radius+1; dy++) {
                    double dist = hypot(dx, dy);
                    double dist_fac = interp(dist, 0, radius, 1, 0);

                    if (dist_fac > 0) {
                        dist_fac = dbounds(dist_fac, 0, 1);
                        int cx = x+dx, cy = y+dy;
                        double fac = intensity * pow(dist_fac, 2);

                        bloom.add(cx, cy, img.get(cx, cy).mult(fac));
                    }
                }
            }
        }
    }

    for (int x = 0; x < img.width; x++) {
        for (int y = 0; y < img.height; y++) {
            double b = bloom.get(x, y).r;
            if (b > 1e9)
                std::cerr << b << std::endl;
            img.add(x, y, bloom.get(x, y));
        }
    }
}


/**
 * Composite an image.
 *
 * @param in_data  Input float image.
 * @param out_data  Output char image.
 */
extern "C" void composite(
    DImg in_data, CImg out_data, int width, int height,
    double p_comp_shutter, double p_comp_bloomInt, double p_comp_bloomRad,
    double p_comp_bloomThres
) {
    ImageD input(in_data, width, height);
    ImageC output(out_data, width, height);

    add_bloom(input, p_comp_bloomInt, p_comp_bloomRad, p_comp_bloomThres);
    double_to_char(input, output, p_comp_shutter);
}
