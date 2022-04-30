#pragma once

#include <algorithm>
#include <cmath>


namespace Pianoray {


constexpr double PI = 3.14159;


double hypot(double x, double y) {
    return pow(x*x + y*y, 0.5);
}

int ibounds(int v, int min, int max) {
    return std::min(std::max(v, min), max);
}

double dbounds(double v, double min, double max) {
    return std::min(std::max(v, min), max);
}

double interp(double v, double old_min, double old_max,
    double new_min, double new_max)
{
    double fac = (v-old_min) / (old_max-old_min);
    return new_min + fac * (new_max-new_min);
}


}  // namespace Pianoray
