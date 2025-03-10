#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*
Extend the smooth function to be applicable to a 2D array, for which
the numerical formula is
*/

void smooth_inplace(int** arr, int h, int w, int c) {
    // Apply the smooth function in place
    int vij, vup, vleft, vright, vdown;
    for (int i=0; i<h; i++) {
        for (int j=0; j<w; j++) {
            vij = arr[i][j];
            vup = (i > 0) ? arr[i-1][j] : 0;
            vleft = (j > 0) ? arr[i][j-1] : 0;
            vright = (j < w-1) ? arr[i][j+1] : 0;
            vdown = (i < h-1) ? arr[i+1][j] : 0;
            arr[i][j] = vij + c*(vup + vleft - 4*vij + vright + vdown);
        }
    }
}

int** smooth_matrix(int** src, int h, int w, int c) {
    /*
    This pure function initiates a new matrix with the smooth operation applied
    */
    int** new_arr = malloc(h*sizeof(int*));
    for (int i=0; i<h; i++) {
        new_arr[i] = malloc(w*sizeof(int));
        memcpy(new_arr[i], src[i], w);
    }

    smooth_inplace(new_arr, h, w, c);
    return new_arr;
}

int main() {
    int h = 5;
    int w = 5;
    int c = 5;

    int** matrix = malloc(h*sizeof(int*));
    for (int i=0; i<h; i++) {
        matrix[i] = malloc(w*sizeof(int));
        for (int j=0; j<w; j++) {
            matrix[i][j] = i*w+j;
        }
    }

    int** sm = smooth_matrix(matrix, h, w, c);

    free(matrix);
    free(sm);

    return 0;
}
