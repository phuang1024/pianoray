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


namespace Random {


constexpr int LARGE = (int)1e9;


/**
 * Float between 0 and 1.
 */
double random() {
    int r = rand() % LARGE;
    return (double)r / LARGE;
}

/**
 * Float between a and b.
 */
double uniform(double a, double b) {
    return a + (b-a) * random();
}

/**
 * Integer in [a, b)
 */
int randint(int a, int b) {
    int delta = (b-a) * random();
    return a + delta;
}


}  // namespace Random
