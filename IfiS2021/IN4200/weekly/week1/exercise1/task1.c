#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
Write a C program to verify that the limit of ...
*/

int main(int argc, char* argv[]) {
  int n = atoi(argv[1]);

  double sigma = 0;

  for (int i=0; i<n; i+=4)
    sigma += (1/pow(2, i)) - (1/pow(2, i+2));

  printf("The value converges towards %f with %d itearations\n", sigma, n);

  return 0;
}
