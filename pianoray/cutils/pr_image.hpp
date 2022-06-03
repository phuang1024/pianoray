#pragma once

#include "pr_math.hpp"


/**
 * RGB color.
 */
template<class T>
struct Color {
    T r, g, b;

    /**
     * Initialize all 0.
     */
    Color() {
        r = g = b = 0;
    }

    /**
     * Initialize with given values.
     */
    Color(T r, T g, T b) {
        this->r = r;
        this->g = g;
        this->b = b;
    }

    /**
     * Initialize from rgb data.
     */
    Color(T* data) {
        r = data[0];
        g = data[1];
        b = data[2];
    }

    Color(const Color<T>& other) {
        this->r = other.r;
        this->g = other.g;
        this->b = other.b;
    }

    /**
     * Get r, g, b based on i = 0, 1, 2
     * Returns 0 if i != 0, 1, 2
     */
    T get(int i) const {
        if (i == 0)
            return r;
        if (i == 1)
            return g;
        if (i == 2)
            return b;
        return 0;
    }

    /**
     * Set a value.
     * Does nothing if i != 0, 1, 2
     */
    void set(int i, T v) {
        if (i == 0)
            r = v;
        else if (i == 1)
            g = v;
        else if (i == 2)
            b = v;
    }
};


template<class T>
class Image {
public:
    Color<T>* data;
    int width, height;

    /**
     * Initialize.
     * @param data  Memory of values.
     *              Shape should be (height, width, channel)
     */
    Image(T* data, int width, int height) {
        this->data = (Color<T>*)data;
        this->width = width;
        this->height = height;
    }

    /**
     * Index of data for corresponding coords.
     */
    int index(int x, int y) const {
        return y*width + x;
    }

    /**
     * Get value at coord.
     */
    Color<T> get(int x, int y) const {
        return data[index(x, y)];
    }

    /**
     * Set value to color.
     */
    void set(int x, int y, const Color<T>& c) {
        data[index(x, y)] = c;
    }
};


// Lexical parser Python-side will see these instead of pointers and
// will know that expected numpy array dimension is 3.
using CImg = unsigned char*;
using DImg = double*;

using ColorC = Color<unsigned char>;
using ColorD = Color<double>;
using ImageC = Image<unsigned char>;
using ImageD = Image<double>;
