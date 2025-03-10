#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
Write a C program that allocates a 1D array of length n which is
prescribed at runtime. You are supposed to first assign the values
of the array with random numbers, and then find the maximum and
minimum values. (You can use e.g. the rand function from stdlib.h.)
*/

int min(int* a, int size) {
    int n = a[0];
    for (int i=1; i<size; i++)
        if (n < a[i]) n = a[i];
    return n;
}

int max(int* a, int size) {
    int n = a[0];
    for (int i=1; i<size; i++)
        if (n > a[i]) n = a[i];
    return n;
}

int main(int argc, char* argv[]) {
    int n = atoi(argv[1]);
    int* arr = malloc(n*sizeof(int));

    for (int i=0; i<n; i++)
        arr[i] = rand();

    printf("Generated array:\n[");

    for (int i=0; i<n-1; i++)
        printf("%d, ", arr[i]);

    printf("%d", arr[n-1]);
    puts("]");
    printf("Min: %d\n", min(arr, n));
    printf("Max: %d\n", max(arr, n));
    free(arr);
    return 0;
}
