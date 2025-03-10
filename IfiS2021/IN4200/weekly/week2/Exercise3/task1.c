#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define SIZE_DEFAULT 500



double*** init_3tensor(int nx, int ny, int nz) {
    double*** A = malloc(sizeof(double*)*nx);
    A[0] = malloc(sizeof(double*)*nx*ny);
    A[0][0] = malloc(sizeof(double)*nx*ny*nz);
    for (int i=1; i<nz; i++) A[i] = &A[0][ny*i];
    for (int j=1; j<nz*ny; j++) A[0][j] = &A[0][0][j*nx];
    return A;
}

double*** zero_3tensor(int nx, int ny, int nz) {
    double*** A = malloc(sizeof(double*)*nx);
    A[0] = malloc(sizeof(double*)*nx*ny);
    A[0][0] = calloc(sizeof(double), nx*ny*nz);
    for (int i=1; i<nz; i++) A[i] = &A[0][ny*i];
    for (int j=1; j<nz*ny; j++) A[0][j] = &A[0][0][j*nx];
    return A;
}

int main(int argc, char const *argv[]) {
    int nx, ny, nz;
    nx = (argc > 1) ? atoi(argv[1]) : SIZE_DEFAULT;
    ny = (argc > 2) ? atoi(argv[2]) : SIZE_DEFAULT;
    nz = (argc > 3) ? atoi(argv[3]) : SIZE_DEFAULT;

    double*** v = init_3tensor(nx, ny, nz);

    double denominator = (nx-1)*(ny-1)*(nz-1);

    for (int i=0; i<nx; i++)
        for (int j=0; j<ny; j++)
            for (int k=0; k<nz; k++)
                v[i][j][k] = 2.0 + sin((i * j * k * M_PI) / denominator);


    double*** u = zero_3tensor(nx, ny, nz);

    for (int i=1; i<nx-2; i++)
        for (int j=1; j<ny-2; j++)
            for (int k=1; k<nz-2; k++) {
                double vijk, sum;
                sum = 0;
                vijk = v[i][j][k];
                for (int l=-1; l<2; l+=2)
                    sum += v[i+l][j][k] + v[i][j+l][k] + v[i][j][k+l];
                sum -= 6 * vijk;
                u[i][j][k] = vijk + sum/6;
                v[i][j][k] = u[i][j][k];
            }

    free(u[0][0]);
    free(u[0]);
    free(u);

    free(v[0][0]);
    free(v[0]);
    free(v);
    return 0;
}
