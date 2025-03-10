#include <stdio.h>

void display_vector(int* v, int len) {
    printf("[");
    for (int i=0; i<len-1; i++)
        printf("%d, ", v[i]);
    printf("%d", v[len-1]);
    printf("]");
}


void display_matrix(int** arr, int m, int n) {
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
