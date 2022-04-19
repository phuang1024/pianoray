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

#include <algorithm>
#include <cmath>


namespace Pianoray {


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
