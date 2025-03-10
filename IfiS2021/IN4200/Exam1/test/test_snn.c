#include <stdio.h>
#include <stdlib.h>
#include "../src/snn.h"
#include "../src/utils.h"

#define SIMPLE_GRAPH "data/simple-graph.txt"

int test_read_graph_from_file1() {
    puts("*** TESTING read_graph_from_file1 ***");

    int failed = 0;
    int N;
    char **table2D;
    read_graph_from_file1(SIMPLE_GRAPH, &N, &table2D);

    display_matrix(table2D, N, N);

    if (N != 5) fprintf(stderr, "FAILED: N should be 5, was %d\n", N);

    char expected_matrix[5][5] = {
        { 0, 1, 1, 1, 0 },
        { 1, 0, 1, 1, 0 },
        { 1, 1, 0, 1, 1 },
        { 1, 1, 1, 0, 1 },
        { 0, 0, 1, 1, 0 }
    };

    for (int i=0; i<N; i++) {
        for (int j=0; j<N; j++) {
            if (table2D[i][j] != expected_matrix[i][j]) {
                fprintf(
                    stderr,
                    "FAILED: talbe2D[%d][%d] was %d instead of %d\n",
                    i, j, table2D[i][j], expected_matrix[i][j]
                );
                failed += 1;
            }
        }
    }

    if (failed) {
        puts("*** read_graph_from_file1 FAILED ***");
    } else {
        puts("*** read_graph_from_file1 PASSED ***");
    }

    free(table2D[0]);
    free(table2D);
    return failed;
}

int test_read_graph_from_file2() {
    puts("*** TESTING read_graph_from_file2 ***");
    int failed = 0;
    int *row_ptr;
    int *col_idx;
    int N;
    read_graph_from_file2(SIMPLE_GRAPH, &N, &row_ptr, &col_idx);
    if (N != 5) fprintf(stderr, "FAILED: N should be 5, was %d\n", N);

    int expected_row_ptr[6] = {0, 3, 6, 10, 14, 16};

    for (int i=0; i<N+1; i++) {
        if (expected_row_ptr[i] != row_ptr[i]) {
            fprintf(
                stderr,
                "FAILED: row_ptr[%d] was %d instead of %d\n",
                row_ptr[i], expected_row_ptr[i]
            );
            failed++;
        }
    }

    int expected_col_idx[16] = {1, 2, 3, 0, 2, 3, 0, 1, 3, 4, 0, 1, 2, 4, 2, 3};

    for (int i=0; i<16; i++) {
        if (expected_col_idx[i] != col_idx[i]) {
            fprintf(
                stderr,
                "FAILED: col_idx[%d] was %d instead of %d\n",
                col_idx[i], expected_col_idx[i]
            );
            failed++;
        }
    }

    free(row_ptr);
    free(col_idx);

    if (failed) {
        puts("*** read_graph_from_file2 FAILED ***");
    } else {
        puts("*** read_graph_from_file2 PASSED ***");
    }

    return 0;
}

int test_create_SNN_graph1() {
    int failed = 0;
    puts("*** TESTING create_SNN_graph1 ***");
    int N;
    char **table2D;
    read_graph_from_file1(SIMPLE_GRAPH, &N, &table2D);

    int **SNN_table;
    create_SNN_graph1(N, table2D, &SNN_table);
    display_int_matrix(SNN_table, N, N);

    int expected_matrix[5][5] = {
        {0, 2, 2, 2, 0},
        {2, 0, 2, 2, 0},
        {2, 2, 0, 3, 1},
        {2, 2, 3, 0, 1},
        {0, 0, 1, 1, 0}
    };

    for (int i=0; i<N; i++) {
        for (int j=0; j<N; j++) {
            if (SNN_table[i][j] != expected_matrix[i][j]) {
                fprintf(
                    stderr,
                    "FAILED: SNN_table[%d][%d] was %d instead of %d\n",
                    i, j, SNN_table[i][j], expected_matrix[i][j]
                );
                failed += 1;
            }
        }
    }

    free(SNN_table[0]);
    free(SNN_table);
    free(table2D[0]);
    free(table2D);

    if (failed) {
        puts("*** read_graph_from_file1 FAILED ***");
    } else {
        puts("*** read_graph_from_file1 PASSED ***");
    }
    return failed;
}

int test_create_SNN_graph2() {
    // UNIT TEST WITH FIXED VALUE EXPECTATION
    puts("*** TESTING create_SNN_graph2 ***");
    int *row_ptr;
    int *col_idx;
    int N;
    read_graph_from_file2(SIMPLE_GRAPH, &N, &row_ptr, &col_idx);

    int *SNN_val;
    create_SNN_graph2(N, row_ptr, col_idx, &SNN_val);
    puts("\nOUTPUT:");
    display_int_vector(SNN_val, 16);
    puts("");

    int vals[] = {2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 3, 1, 1, 1};
    int fail = 0;
    for (int i=0; i<16; i++) {
        if (SNN_val[i] != vals[i]) {
            fprintf(stderr, "FAILED TEST: VALUES NOT EQUAL TARGET ARRAY: %d != %d\n", SNN_val[i], vals[i]);
            fail = 1;
        }
    }

    free(SNN_val);
    free(col_idx);
    free(row_ptr);
    if (fail) return 1;
    return 0;
}


int test_clustering() {
    // Unmeasurable test as it prints out to terminal
    puts("*** TESTING CLUSTERING ***");
    int n_edges = 16;
    int n_nodes = 5;

    int vals[] = {2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 3, 1, 1, 1};
    int *SNN_val = malloc(sizeof(int)*n_edges);
    for (int i=0; i<n_edges; i++) SNN_val[i] = vals[i];

    int idxs[] = {1, 2, 3, 0, 2, 3, 0, 1, 3, 4, 0, 1, 2, 4, 2, 3};
    int *col_idx = malloc(sizeof(int)*n_edges);
    for (int i=0; i<n_edges; i++) col_idx[i] = idxs[i];

    int rows[] = {0, 3, 6, 10, 14, 16};
    int *row_ptr = malloc(sizeof(int)*(n_nodes+1));
    for (int i=0; i<(n_nodes+1); i++) row_ptr[i] = rows[i];

    int tau = 2;
    int node_id = 0;
    printf("\nTesting with threshold tau=%d on node %d\n", tau, node_id);
    check_node(node_id, tau, n_nodes, row_ptr, col_idx, SNN_val);

    tau = 1;
    node_id = 0;
    printf("\nTesting with threshold tau=%d on node %d\n", tau, node_id);
    check_node(node_id, tau, n_nodes, row_ptr, col_idx, SNN_val);


    tau = 2;
    node_id = 4;
    printf("\nTesting with threshold tau=%d on node %d\n", tau, node_id);
    check_node(node_id, tau, n_nodes, row_ptr, col_idx, SNN_val);

    tau = 1;
    node_id = 4;
    printf("\nTesting with threshold tau=%d on node %d\n", tau, node_id);
    check_node(node_id, tau, n_nodes, row_ptr, col_idx, SNN_val);

    tau = 3;
    node_id = 3;
    printf("\nTesting with threshold tau=%d on node %d\n", tau, node_id);
    check_node(node_id, tau, n_nodes, row_ptr, col_idx, SNN_val);



    free(SNN_val);
    free(row_ptr);
    free(col_idx);

    return 0;
}

int main(int argc, char *argv[]) {
    char *filename = argc < 2 ? "data/simple-graph.txt" : argv[1];

    test_read_graph_from_file1();

    test_read_graph_from_file2();


    test_create_SNN_graph1();

    test_create_SNN_graph2();

    test_clustering();


    return 0;
}
