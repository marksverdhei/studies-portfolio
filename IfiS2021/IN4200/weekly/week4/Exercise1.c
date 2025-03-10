#include <stdio.h>
#include <stdlib.h>

double* scale_vector(double s, double* b, size_t N) {
    double* a = malloc(sizeof(double)*N);
    int i;
    for (i=0; i<N; i++)
        a[i] = s*b[i];

    return a;
}


int main(int argc, char const *argv[]) {
    int size;
    if (argc > 1) {
        size = atoi(argv[1]);
    } else {
        size = 10;
    }

    double* v = malloc(sizeof(double)*);
    

    return 0;
}
