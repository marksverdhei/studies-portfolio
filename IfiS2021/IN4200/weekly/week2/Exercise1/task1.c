#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
Write a simple C program that illustrates the speed advantages of reading
and writing binary data files, compared with using ASCII data files.
*/

// TODO: FIND OUT WHY THIS DOESN'T WORK
#define TO_MS(t) ((1000*t)/CLOCKS_PER_SEC)

static int n = 50000;

int equal_arrays(int* a, int* b, size_t size) {
    for (size_t i=0; i<size; i++) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

void write_data(char* filename, char* flag) {
    FILE* fp = fopen(filename, flag);
    if (fp == NULL) {
        printf("FAILED TO OPEN FILE %s\n", filename);
        exit(1);
    }
    size_t arrsize = sizeof(int)*n;
    int* ints = malloc(arrsize);
    for (int i=0; i<n; i++) ints[i] = i;

    fwrite(ints, arrsize, sizeof(int), fp);
    free(ints);
    fclose(fp);
}

int* read_data(char* filename, char* flag) {
    FILE* fp = fopen(filename, flag);
    if (fp == NULL) {
        printf("FAILED TO OPEN FILE %s\n", filename);
        exit(1);
    }

    size_t arrsize = sizeof(int)*n;
    int* ints = malloc(arrsize);

    fread(ints, sizeof(int), n, fp);

    fclose(fp);
    return ints;
}

void benchmark() {
    char* metadata[2][3] = {
        "asciis.txt",
        "w+",
        "r",
        "binaries.bin",
        "wb+",
        "rb",
    };

    clock_t start, mid, end;
    int* ints[2];

    for (int i=0; i<2; i++) {
        char* filename = metadata[i][0];
        char* w_flag = metadata[i][1];
        char* r_flag = metadata[i][2];
        start = clock();
        write_data(filename, w_flag);
        mid = clock();
        int* data = read_data(filename, r_flag);
        end = clock();
        printf("File: %s\n", filename);
        printf("Time elapsed for writing: %lu ms\n", TO_MS(mid-start));
        printf("Time elapsed for reading: %lu ms\n", TO_MS(end-mid));
        printf("Total: %lu ms\n", TO_MS(end-start));
        ints[i] = data;
    }

    if (equal_arrays(ints[0], ints[1], n)) {
        puts("ARRAYS ARE EQUAL");
    } else {
        puts("ARRAYS ARE NOT EQUAL");
    }

    for (int i=0; i<2; i++) {
        free(ints[i]);
    }
}

int main() {
    benchmark();
    return 0;
}
