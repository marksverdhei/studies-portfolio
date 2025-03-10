#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
Write a C program that allocates a 3D array of dimension (nx, ny, nz).
A 1D underlying contiguous storage should be used. Assign the values
of the 3D array, such as u[i][j][k]=i*n y*n z+j*n z+k. Deallocate
the 3D array at the end of the program
*/

int main(int argc, char* argv[]) {
    if (argc < 4) {
        puts("ERROR: supply arguments x, y and z");
        exit(1);
    }

    int nx, ny, nz;
    nx = atoi(argv[1]);
    ny = atoi(argv[2]);
    nz = atoi(argv[3]);

    if (nx <= 0 || ny <= 0 || nz <= 0) {
        puts("ERROR: arguments must be integers above zero");
    }

    int size = nx*ny*nz;
    printf("Size: %d\n", size);
    int* tensor = malloc(size*sizeof(int));

    for (int i=0; i<nx; i++) {
        for (int j=0; j<ny; j++) {
            for (int k=0; k<nz; k++) {
                int current_index = i*ny*nz+j*nz+k;
                tensor[current_index] = i*ny*nz+j*nz+k;
            }
        }
    }

    free(tensor);
    return 0;
}
