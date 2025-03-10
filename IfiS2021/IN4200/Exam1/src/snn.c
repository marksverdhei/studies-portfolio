#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include "utils.h"

#define BUFFER_SIZE 256

#define INVALID_LINK(i, j) ( \
            i == j \
            || i > n_nodes \
            || j > n_nodes \
            || i < 0 \
            || j < 0 \
)

void generic_read_file(FILE *fp, int *n_nodes, int *n_edges) {

    if (fp == NULL) {
        perror("FILE IS NULL: EXITING");
        exit(1);
    }

    // line separator
    char sep[2] = " ";
    char buffer[BUFFER_SIZE];
    // skip first two lines
    // and get important third line
    for (int i=0; i<3; i++) fgets(buffer, BUFFER_SIZE, fp);

    int graph_size[2];
    // parse count lines
    strtok(buffer, sep);
    for (int i=0; i<2; i++) {
        strtok(NULL, sep);
        graph_size[i] = atoi(strtok(NULL, sep));

    }
    // Skip next line
    fgets(buffer, BUFFER_SIZE, fp);

    *n_nodes = graph_size[0];
    *n_edges = graph_size[1];
}

// Exercise 1
void read_graph_from_file1(char *filename, int *N, char ***table2D) {
    /*
    reads through the given file on the expected format and
    constructs a 2-Dimensional character matrix resembling
    an adjacency matrix
    */

    FILE *fp = fopen(filename, "r");
    int n_edges;

    generic_read_file(fp, N, &n_edges);

    int n_nodes = *N;

    char **adj_matrix = create_zero_matrix(n_nodes, n_nodes, sizeof(char));

    char sep[2] = " ";
    char buffer[BUFFER_SIZE];

    int i, j;
    while (fgets(buffer, BUFFER_SIZE, fp) != NULL) {
        i = atoi(strtok(buffer, sep));
        j = atoi(strtok(NULL, sep));

        // Some of the edges may have “illegal” values for FromNodeId and/or ToNodeId,
        // these should be excluded (not used in the data storage later);
        if (INVALID_LINK(i, j)) continue;

        adj_matrix[i][j] = 1;
        adj_matrix[j][i] = 1;
    }
    fclose(fp);

    *table2D = adj_matrix;
}

struct Edge {
    int row, col;
};

int comparator(const void *a, const void *b) {
    struct Edge *x = (struct Edge*)a;
    struct Edge *y = (struct Edge*)b;
    if (x->row < y->row) return -1;
    if (x->row > y->row) return 1;
    // They are equal
    if (x->col < y->col) return -1;
    if (x->col > y->col) return 1;
    return 0;
}


void read_graph_from_file2(char *filename, int *N, int **row_ptr, int **col_idx)  {
    FILE *fp = fopen(filename, "r");

    int n_edges;
    generic_read_file(fp, N, &n_edges);
    int n_nodes = *N;

    char sep[2] = " ";
    char buffer[BUFFER_SIZE];

    // size the graph is undirected we count double the edges
    int total_edges = 2*n_edges;

    struct Edge *coo_matrix = malloc(sizeof(struct Edge)*(total_edges));
    int i, j;
    for (int k=0; k<total_edges; k+=2) {
        fgets(buffer, BUFFER_SIZE, fp);
        i = atoi(strtok(buffer, sep));
        j = atoi(strtok(NULL, sep));

        if (INVALID_LINK(i, j)) continue;

        coo_matrix[k].row = i;
        coo_matrix[k].col = j;

        coo_matrix[k+1].row = j;
        coo_matrix[k+1].col = i;
    }

    fclose(fp);

    qsort(coo_matrix, n_edges*2, sizeof(struct Edge*), comparator);

    // Now transfer from coo to csr
    // int *coo_ints = (int*)coo_matrix;
    int *csr_col = malloc(sizeof(int)*(total_edges+1));
    csr_col[total_edges] = -1;
    int *csr_row = calloc(n_nodes+1, sizeof(int));

    for (int i=0; i<total_edges; i++) {
        csr_col[i] = coo_matrix[i].col;
        csr_row[coo_matrix[i].row+1]++;
    }

    for (int i = 0; i < n_nodes; i++)
        csr_row[i + 1] += csr_row[i];

    *row_ptr = csr_row;
    *col_idx = csr_col;

    free(coo_matrix);
}



// Exercise 2
void create_SNN_graph1(int N, char **table2D, int ***SNN_table) {
    /*
    SNN table as output (to be allocated inside the function, thus triple pointer as type)

    Approach: everything with read-only access can be accessed in parallel.
    Therefore, only the writing is critical

    Since the matrix is symmetrical, we only need to access the upper triangle for the
    computations
    */
    int** snn_matrix = create_zero_matrix(N, N, sizeof(int));

    #ifdef _OPENMP
        # pragma omp parallel for
    #endif
    for (int i=0; i<N; i++) {
        for (int j=i+1; j<N; j++) {
            // snn_row = snn_matrix[i];
            // for (int k=0; k<N; k++) snn_matrix[i][j] += (table2D[i][j] && table2D[i][k] && table2D[j][k]);
            for (int k=0; k<N; k++) if (table2D[i][j]) {
                snn_matrix[i][j] += (table2D[i][k] && table2D[j][k]);
                snn_matrix[j][i] = snn_matrix[i][j];
            }
        }
    }

    *SNN_table = snn_matrix;
}

void create_SNN_graph2(int N, int *row_ptr, int *col_idx, int **SNN_val) {
    int n_edges = 0;
    while (col_idx[n_edges] != -1) n_edges++;
    int *values = calloc((n_edges+1), sizeof(int));
    values[n_edges] = -1;
    int *row_ptr_gaps = malloc(sizeof(int)*(N+1));
    for (int i=0; i<N; i++) row_ptr_gaps[i] = row_ptr[i+1]-row_ptr[i];
    row_ptr_gaps[N] = N-row_ptr_gaps[N-1];

    int gap1, ptr_start1, ptr_end1;
    int gap2, ptr_start2, ptr_end2;

    // #ifdef _OPENMP
    //     #pragma omp parallel for
    // #endif
    for (int row_num1=0; row_num1<N; row_num1++) {
        gap1 = row_ptr_gaps[row_num1];
        if (gap1 < 1) continue;
        ptr_start1 = row_ptr[row_num1];
        ptr_end1 = ptr_start1 + gap1;
        for (int nb1=ptr_start1; nb1<ptr_end1; nb1++) {
            int row_num2 = col_idx[nb1];
            // we already know gap2 is 1 or greater
            gap2 = row_ptr_gaps[row_num2];
            ptr_start2 = row_ptr[row_num2];
            ptr_end2 = ptr_start2 + gap2;
            // compare neigbors
            int i=ptr_start1;
            int j=ptr_start2;
                while (i < ptr_end1 && j < ptr_end2) {
                    int col_i = col_idx[i];
                    int col_j = col_idx[j];
                    if (col_i < col_j) {
                        i++;
                    } else if (col_j < col_i) {
                        j++;
                    } else {
                        values[j]++;
                        i++;
                        j++;
                    }
                }
        }
    }

    free(row_ptr_gaps);

    *SNN_val = values;
}

void traverse_node(int id, int *visited_nodes, int tau, int N, int *row_ptr_nz, int *col_idx, int *SNN_val) {
    visited_nodes[id] = 1;
    int start = row_ptr_nz[id];
    if (start == -1) {
        perror("Unexpected event: traversed island node");
        exit(1);
    }

    int end = start;
    for (int i=id+1; i<N; i++) {
        if (row_ptr_nz[i] != -1) {
            end = row_ptr_nz[i];
            break;
        }
    }

    for (int i=start; i<end; i++) {
        if (SNN_val[i] >= tau) {
            int neighbor_id = col_idx[i];
            if (visited_nodes[neighbor_id] == 0)
                traverse_node(neighbor_id, visited_nodes, tau, N, row_ptr_nz, col_idx, SNN_val);
        }
    }
}

// Exercise 3
void check_node(int node_id, int tau, int N, int *row_ptr, int *col_idx, int *SNN_val) {
    // according to this, using int over char for boolean expressions can actually be faster
    // https://stackoverflow.com/questions/9521140/char-or-int-for-boolean-value-in-c#:~:text=There%20is%20a%20_Bool%20in,using%20char%20are%20likely%20negligible.
    int *visited_nodes = calloc(N, sizeof(int));

    // make a copy of row_ptr that marks all zeroed rows
    int *row_ptr_nz = malloc((N+1)*sizeof(int));

    row_ptr_nz[0] = row_ptr[0];

    for (int i=1; i<N+1; i++) {
        if (row_ptr[i] == row_ptr[i-1]) {
            row_ptr_nz[i] = -1;
        } else {
            row_ptr_nz[i] = row_ptr[i];
        }
    }

    traverse_node(node_id, visited_nodes, tau, N, row_ptr_nz, col_idx, SNN_val);

    int cluster_size = 0;
    printf("Node ");
    for (int i=0; i<N; i++) {
        cluster_size += visited_nodes[i];
        if (visited_nodes[i]) printf("\n  %d,", i);
    }

    if (cluster_size > 1) {
        puts(" are all members of found cluster");
    } else {
        puts(" is not a member of any cluster");
    }

    free(visited_nodes);
    free(row_ptr_nz);
}
