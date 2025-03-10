#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
/*
Find out the highest and lowest temperatures and when they occurred.
Compute also the average temperature and the associated standard deviation
*/

struct temp {
    char* time;
    float temp;
};


struct temp* read_data(char* filename, int* out_size) {
    FILE* fp = fopen(filename, "r");
    if (fp == NULL) {
      printf("ERROR! File \"%s\" not found! exiting...\n", filename);
      exit(1);
    }

    char buffer[100];
    int size = 10;
    struct temp* temperatures = malloc(size*sizeof(struct temp));

    int count = 0;
    while (fgets(buffer, 100, fp) != NULL) {
        if (count >= size) {
            size *= 2;
            temperatures = realloc(temperatures, size*sizeof(struct temp));
            if (!temperatures) puts("FAILED TO REALLOC");
        }

        char* time = strtok(buffer, " ");
        float temp = atof(strtok(NULL, " "));

        char* s = malloc(5*sizeof(char));
        s = strcpy(s, time);
        temperatures[count].time = s;
        temperatures[count].temp = temp;
        printf("Time: %s, temp: %f\n", s, temp);
        count++;
    }

    fclose(fp);

    // TODO: Find out why this corrupts array
    // temperatures = realloc(temperatures, (count)*sizeof(struct temp*));
    *out_size = count;
    return temperatures;
}


void min_max_mean_std(float* arr, int size, int* min_i, int* max_i, float* mean, float* std) {
    // set input vars to zero

    int mni = 0;
    int mxi = 0;
    float mu = 0.0;
    float sig = 0.0;

    printf("%d, %d, %f, %f\n", mni, mxi, mu, sig);
    for (int i=0; i<size; i++) {
        printf("Iteration %d, t=%f\n", i, arr[i]);
        mu += (float)arr[i];
        if (arr[mni] > arr[i]) mni = i;
        if (arr[mxi] < arr[i]) mxi = i;
    }

    mu /= size;
    printf("Mean: %f\n", mu);

    for (int i=0; i<size; i++) sig += pow(arr[i]-mu, 2);
    sig /= size;
    sig = sqrt(sig);

    *min_i = mni;
    *max_i = mxi;
    *mean = mu;
    *std = sig;
}


int main() {
    int size;
    struct temp* measures = read_data("generated_temps.csv", &size);
    printf("%d\n", size);
    float* temps = malloc(sizeof(float)*size);

    // Copy temperatures
    for (int i=0; i<size; i++) {
        // printf("measures[i].temp = %f\n", measures[i].temp);
        temps[i] = measures[i].temp;
        // printf("temps[i] = %f\n", temps[i]);

    }
    // find max and min temp, compute mean and stdev
    int max_idx, min_idx;
    float mean, stdev;
    min_max_mean_std(temps, size, &min_idx, &max_idx, &mean, &stdev);

    printf("The hottest time of the day was %s with a temperature of %f\n", measures[max_idx].time, temps[max_idx]);
    printf("The coldest time of the day was %s with a temperature of %f\n", measures[min_idx].time, temps[min_idx]);

    printf("Mean temperature through the day: %f, std: %f\n", mean, stdev);

    free(measures);
    free(temps);
    return 0;
}
