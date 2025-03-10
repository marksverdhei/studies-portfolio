#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/*
When assigning values to the entries of a m × n matrix, it is common
to use a nested for-loop with the outer index looping over the rows
and the inner index looping over the columns. Does it matter if the
sequence of these two loops is swapped? Write a C program to test
your hypothesis.

A: yes it matters because of physical array alignment.
./task3 20000 20000
Generated matrix
Randomizing matrix:
Summing horizontally:
Sum: 1324455390; Time elapsed: 1
Summing vertically
Sum: 1324455390; Time elapsed: 8

Yes i am aware that the sums are most likely incorrect because of numerical overflow

*/

int** zero_matrix(int m, int n)
{
    int** arr = calloc(m, sizeof(int*));
    for (int i=0; i<m; i++)
        arr[i] = calloc(n, sizeof(int));

    return arr;
}

void free_matrix(int** arr, int m, int n)
{
    for (int i=0; i<m; i++)
        free(arr[i]);

    free(arr);
}

void randomize_matrix(int** arr, int m, int n)
{
    for (int i=0; i<m; i++)
        for (int j=0; j<n; j++)
            arr[i][j] = (rand()/1000);
}

void display_vector(int* v, int len)
{
    printf("[");
    for (int i=0; i<len-1; i++)
        printf("%d, ", v[i]);
    printf("%d", v[len-1]);
    printf("]");
}

void display_matrix(int** arr, int m, int n)
{
    printf("[");
    display_vector(arr[0], n);
    printf("\n");
    for (int i=1; i<m-1; i++)
    {
        printf(" ");
        display_vector(arr[i], n);
        printf("\n");
    }
    printf(" ");
    display_vector(arr[m-1], n);
    printf("]\n");
}

int sum_horizontally(int** arr, int m, int n)
{
    int sigma = 0;
    for (int i=0; i<m; i++)
    {
        for (int j=0; j<n; j++)
        {
            sigma += arr[i][j];
        }
    }
    return sigma;
}

int sum_vertically(int** arr, int m, int n)
{
    int sigma = 0;
    for (int j=0; j<n; j++)
    {
        for (int i=0; i<m; i++)
        {
            sigma += arr[i][j];
        }
    }
    return sigma;
}

int main(int argc, char* argv[])
{
    int n = atoi(argv[1]);
    int m = atoi(argv[2]);

    int** arr = zero_matrix(m, n);

    puts("Generated matrix");
    // display_matrix(arr, m, n);
    puts("Randomizing matrix:");
    randomize_matrix(arr, m, n);

    time_t h_time, v_time;
    int sum;
    puts("Summing horizontally:");
    h_time = time(NULL);
    sum = sum_horizontally(arr, m, n);
    h_time = time(NULL) - h_time;
    printf("Sum: %d; Time elapsed: %d\n", sum, h_time);

    puts("Summing vertically");
    v_time = time(NULL);
    sum = sum_vertically(arr, m, n);
    v_time = time(NULL) - v_time;
    printf("Sum: %d; Time elapsed: %d\n", sum, v_time);

    return 0;
}
