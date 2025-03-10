
void single_layer_convolution(
    int M,
    int N,
    float **input,
    int K,
    float **kernel,
    float **output
) {
    /*

    */
    int i,j,ii,jj;
    double temp;

    for (i=0; i<=M-K; i++) {
        for (j=0; j<=N-K; j++) {
            temp = 0.0;
            for (ii=0; ii<K; ii++)
                for (jj=0; jj<K; jj++)
                    temp += input[i+ii][j+jj]*kernel[ii][jj];
            output[i][j] = temp;
        }
    }
}

void double_layer_convolution(
    int M,
    int N,
    float **input,
    int K1,
    float **kernel1,
    int K2,
    float **kernel2,
    float **output) {
    /*
    M: number of rows in matrix
    N: number of columns in matrix
    input: input matrix
    K1: kernel dimensions of kernel 1 (K x K)
    kernel1: kernel1 values
    K2: dimensions of kernel 2
    kernel2: kernel2 values
    output: the result matrix
    */
    int i,j,ii,jj;
    double temp;

    

}

void MPI_double_layer_convolution(
    int M,
    int N,
    float **input,
    int K1,
    float **kernel1,
    int K2,
    float **kernel2,
    float **output
) {
    /*

    */


}



int main_mpi(int nargs, char **args) {
    int M=0, N=0, K=0;
    int my_rank;

    float **input = NULL;
    float **output = NULL;
    float **kernel = NULL;

    MPI_Init(&nargs, &args);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    if (my_rank == 0) {
        // read from command line the values of M, N, and K
        // allocate 2D array ’input’ with M rows and N columns
        // allocate 2D array ’output’ with M-K+1 rows and N-K+1 columns
        // allocate the convolutional kernel with K rows and K columns
        // fill 2D array ’input’ with some values
        // fill kernel with some values
        // ....
    }
    // process 0 broadcasts values of M, N, K to all the other processes
    // ...
    if (my_rank > 0) {
        // allocated the convolutional kernel with K rows and K columns
        // ...
    }
    // process 0 broadcasts the content of kernel to all the other processes
    // ...
    // parallel computation of a single-layer convolution
    MPI_double_layer_convolution(M, N, input, K, kernel, output);

    if (my_rank == 0) {
        // For example, compare the content of array ’output’ with that is
        // produced by the sequential function single_layer_convolution
        // 3
        // ...
    }

    MPI_Finalize();
    return 0;
}


int main(int argc, char **argv) {
    return main_mpi(argc, argv);
}
