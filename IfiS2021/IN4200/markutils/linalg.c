#include <stdlib.h>


void** create_matrix(int h, int w, size_t dtype_size) {
    /*
    h: height
    w: width
    */
    void** A = malloc(sizeof(void*) * h);
    A[0] = malloc(dtype_size * h * w);
    for (int i=1; i<w; i++) A[i] = &A[0][i*h*dtype_size];
    return A;
}

void** create_zero_matrix(int h, int w, size_t dtype_size) {
    void** A = malloc(sizeof(void*) * h);
    A[0] = calloc(h * w, dtype_size);
    for (int i=1; i<w; i++) A[i] = &A[0][i*h*dtype_size];
    return A;
}

void*** create_3tensor(int h, int w, int d, size_t dtype_size) {
    /*
    h: height
    w: width
    d: depth
    */
    void*** T = malloc(sizeof(void*) * h);
    T[0] = malloc(sizeof(void*) * h * w);
    T[0][0] = malloc(dtype_size * h * w * d);
    for (int i=1; i<d; i++) T[i] = &T[0][w*i];
    for (int j=1; j<d*w; j++) T[0][j] = &T[0][0][j * h * dtype_size];
    return T;
}

void*** create_zero_3tensor(int h, int w, int d, size_t dtype_size) {
    /*

    */
    double*** T = malloc(sizeof(void*)*h);
    T[0] = malloc(sizeof(double*)*h*w);
    T[0][0] = calloc(h*w*d, dtype_size);
    for (int i=1; i<d; i++) T[i] = &T[0][w*i];
    for (int j=1; j<d*w; j++) T[0][j] = &T[0][0][j * h * dtype_size];
    return T;
}
