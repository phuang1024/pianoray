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
    const int width = img.width, height = img.height;

    // Will be added to original image.
    ImageD bloom(width, height);

    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height/2; y++) {
            const ColorD col = img.get(x, y);
            double mag = (col.r+col.g+col.b) / 3.0;
            if (!(mag > 0 && mag >= thres))
                continue;

            // Adaptive radius based on brightness.
            const double r = radius * tanh(mag / 5.0);

            const int x_min = dbounds(x-r, 0, width-1);
            const int x_max = dbounds(x+r+1, 0, width-1);
            const int y_min = dbounds(y-r, 0, height-1);
            const int y_max = dbounds(y+r+1, 0, height-1);
            for (int cx = x_min; cx <= x_max; cx++) {
                for (int cy = y_min; cy <= y_max; cy++) {
                    double dist = hypot(cx-x, cy-y);

                    if (dist > 0) {
                        double dist_fac = dbounds(interp(dist, 0, r, 1, 0), 0, 1);
                        double fac = intensity * pow(dist_fac, 2);
                        bloom.max(cx, cy, col.mult(fac));
                    }
                }
            }
        }
    }

    for (int x = 0; x < img.width; x++) {
        for (int y = 0; y < img.height; y++) {
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
