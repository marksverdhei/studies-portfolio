#include <stdio.h>
#include <stdlib.h>

void display_vector(char *v, int len) {
    printf("[");
    for (int i=0; i<len-1; i++)
        printf("%d, ", v[i]);
    printf("%d", v[len-1]);
    printf("]");
}

void display_int_vector(int *v, int len) {
    printf("[");
    for (int i=0; i<len-1; i++)
        printf("%d, ", v[i]);
    printf("%d", v[len-1]);
    printf("]");
}

void display_matrix(char **arr, int m, int n) {
    printf("[");
    display_vector(arr[0], n);
    printf("\n");
    for (int i=1; i<m-1; i++) {
        printf(" ");
        display_vector(arr[i], n);
        printf("\n");
    }
    printf(" ");
    display_vector(arr[m-1], n);
    printf("]\n");
}

void display_int_matrix(int **arr, int m, int n) {
    printf("[");
    display_int_vector(arr[0], n);
    printf("\n");
    for (int i=1; i<m-1; i++) {
        printf(" ");
        display_int_vector(arr[i], n);
        printf("\n");
    }
    printf(" ");
    display_int_vector(arr[m-1], n);
    printf("]\n");
}

void **create_zero_matrix(int h, int w, size_t dtype_size) {
    // Type-generic functon for allocation of zero
    void **A = malloc(sizeof(void*) * h);
    A[0] = calloc(h * w, dtype_size);
    for (int i=1; i<w; i++) A[i] = &A[0][i*h*dtype_size];
    return A;
}
