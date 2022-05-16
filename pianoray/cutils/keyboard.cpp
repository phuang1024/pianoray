#include "pr_image.hpp"
#include "pr_math.hpp"
#include "pr_piano.hpp"
#include "pr_random.hpp"


namespace Pianoray {


/**
 * Render octave lines.
 */
extern "C" void render_octave_lines(UCH* img_data, int width, int height)
{
    Image img(img_data, width, height, 3);
    const int half = height / 2;
    const Color color(80, 80, 80);

    for (int key = 3; key < 88; key += 12) {
        int x = width * (key_pos(key) - 1.0/52.0/2.0);
        for (int y = 0; y < half; y++)
            img.setc(x, y, color);
    }
}


}  // namespace Pianoray
