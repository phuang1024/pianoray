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
