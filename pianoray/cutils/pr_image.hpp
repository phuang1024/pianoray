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
        this->r = r;
        this->g = g;
        this->b = b;
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


using ColorC = Color<unsigned char>;
using ColorD = Color<double>;
using ImageC = Image<unsigned char>;
using ImageD = Image<double>;
