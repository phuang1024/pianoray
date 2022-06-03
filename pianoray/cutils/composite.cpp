#include <cmath>

#include "pr_image.hpp"


/**
 * Composite an image.
 *
 * @param in_data  Input float image.
 * @param out_data  Output char image.
 */
extern "C" void composite(
    double* in_data, unsigned char* out_data, int width, int height
) {
    ImageD input(in_data, width, height);
    ImageC output(out_data, width, height);

    // Use tanh
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            ColorD raw = input.get(x, y);
            ColorC col;
            for (int i = 0; i < 3; i++) {
                double v = tanh(raw.get(i));
                col.set(i, 255 * v);
            }
            output.set(x, y, col);
        }
    }
}
