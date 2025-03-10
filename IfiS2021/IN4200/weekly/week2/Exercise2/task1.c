#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define TO_MS(t) ((1000*t)/CLOCKS_PER_SEC)

int arrays_equal(int* a, int* b, size_t len) {
    for (int i=0; i<len; i++) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

int main(int argc, char const *argv[]) {
    int n = 5000;
    if (argc > 1) {
        n = atoi(argv[1]);
    }

    printf("n=%d\n", n);
    size_t arrsize = sizeof(int)*n;
    int* src = malloc(arrsize);
    int* cpy1 = malloc(arrsize);
    int* cpy2 = malloc(arrsize);

    clock_t t0 = clock();
    memcpy(cpy1, src, arrsize);
    clock_t t1 = clock();
    for (int i=0; i<n; i++) cpy2[i] = src[i];
    clock_t t2 = clock();

    if (!(arrays_equal(src, cpy1, n) && arrays_equal(src, cpy2, n))) {
        puts("ERROR: ARRAYS NOT EQUAL");
    }

    printf("Time elapsed for memcpy: %d ms\n", TO_MS(t1-t0));
    printf("Time elapsed for manual copy: %d ms\n", TO_MS(t2-t1));

    free(src);
    free(cpy1);
    free(cpy2);

    return 0;
}
