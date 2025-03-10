// COMPILE WITH gcc -fopenmp openmp_demo.c -o main
#include <stdio.h>
#include <omp.h>

int main() {
    #pragma omp parallel
    {
        #pragma omp critical
        {
          printf("Hello from thread: %d!\n", omp_get_thread_num());
        }
    }

    return 0;
}
