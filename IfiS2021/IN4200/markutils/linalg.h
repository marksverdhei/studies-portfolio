// generic tensor creation
void** create_matrix(int h, int w, size_t dtype_size);
void** create_zero_matrix(int h, int w, size_t dtype_size);
void*** create_3tensor(int h, int w, int d, size_t dtype_size);
void*** create_zero_3tensor(int h, int w, int d, size_t dtype_size);

void** reshape_to_matrix(int h, int w, int size, size_t dtype_size);

// type specific range
char* c_range(size_t n);
char* c_range_between(size_t k, size_t n);

int* i_range(size_t n);
int* i_range_between(size_t k, size_t n);

float* f_range(size_t n);
float* f_range_between(size_t k, size_t n);

double* d_range(size_t n);
double* d_range_between(size_t k, size_t n);

double* d_linspace(size_t n);
