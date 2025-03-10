#include <iostream>
#include <chrono>
#include <math.h>
using namespace std::chrono;

/*
The standard C math library function
double pow(double x, double y)
returns x raised to the power of y, that is x
y.

This function is very general,
but notoriously slow to execute on a computer.
Please write a special implementation of pow(x,100), that is, when x
is still a floating-point number but the power value y is fixed at integer
100. Only multiplications are needed, and please use as few multiplication
operations as possible.
Write a C program to verify that your special implementation of pow(x,100)
is indeed (much) faster than the standard pow function
*/

double pow100(float x) {
    double prod = x;
    for (int i=0; i<99; i++) prod *= x;
    return prod;
}

int main(int argc, char const *argv[]) {
    if (argc < 2) {
        puts("Supply X as an argument!");
        exit(1);
    }
    float x = atof(argv[1]);

    auto t1 = high_resolution_clock::now();
    double result = pow(x, 100);
    auto t2 = high_resolution_clock::now();
    double result2 = pow100(x);
    auto t3 = high_resolution_clock::now();
    printf("Equal results? %d\n", result == result2);
    printf("%lf\n", result);
    printf("%lf\n", result2);

    auto result_ms = duration_cast<microseconds>(t2 - t1);
    auto result2_ms = duration_cast<microseconds>(t3 - t2);

    printf("Time elapsed for generic pow: %ld micro sec\n", result_ms);
    printf("Time elapsed for pow100: %ld micro sec\n", result2_ms);
    return 0;
}
