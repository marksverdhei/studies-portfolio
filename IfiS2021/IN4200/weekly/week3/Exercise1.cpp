#include <iostream>
#include <chrono>
using namespace std::chrono;

/*
Write a C program that uses the following function for carrying out the
numerical integration of 4
1+x2 between xmin and xmax using a given number
of “slices”:
double numerical_integration (double x_min, double x_max, int slices)
indeed approaches π when the number of “slices” is increased.
Suppose the floating-point division operation can not be pipelined, how
will you use the C program to estimate the latency of a floating-point division
in clock cycles?

To estimate the time consumption of the floating point division, I made an
equivailent function for doing the similar computations, but excluding the
floating point division
*/

double numerical_integration(double x_min, double x_max, int slices) {
    double delta_x = (x_max-x_min)/slices;
    double x, sum = 0.0;
    for (int i=0; i<slices; i++) {
        x = x_min + (i+0.5)*delta_x;
        sum = sum + 4.0/(1.0+x*x);
    }
    return sum * delta_x;
}


double baseline_computation(double x_min, double x_max, int slices) {
    double delta_x = (x_max-x_min)/slices;
    double x, sum = 0.0;
    for (int i=0; i<slices; i++) {
        x = x_min + (i+0.5)*delta_x;
        sum = sum + (1.0+x*x);
    }
    return sum * delta_x;
}


int main(int argc, char* argv[]) {
    if (argc < 2) {
        puts("SUPPLY NUMBER OF SLICES!");
        exit(1);
    }
    puts("Estimating time with numerical intergration");
    auto slices = atoi(argv[1]);
    printf("Number of slices: %d\n", slices);
    auto t1 = high_resolution_clock::now();
    double pi_approx = numerical_integration(0, 1, slices);
    auto t2 = high_resolution_clock::now();
    double baseline_result = baseline_computation(0, 1, slices);
    auto t3 = high_resolution_clock::now();

    printf("Result: %f\n", pi_approx);

    printf("Time elapsed with floating point division: %ld\n", duration_cast<milliseconds>(t2 - t1));
    printf("Time without floating point division: %ld\n", duration_cast<milliseconds>(t3 - t2));

    return 0;
}
