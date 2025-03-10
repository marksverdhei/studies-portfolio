# IN4200 Home exam 1 - Report  
Candidate ID: 15833  

***  

### Note:  

It can be seen in both my report and my code that I use the abbreviation CSR instead of CRS. CSR stands for Compressed Sparse Row and is completely identical in meaning to CRS (Compressed Row Storage). Usage of CSR over CRS just happens to be out of habit.  


## Reading files/matrices  

The more efficient way of creating the csr (compressed sparse row) matrix from
the given file-format is by generating a representation of the matrix in a COO
format, (which the file is, to some extent already in) and then apply a COO to CSR
conversion. This requires sorting, but is still more efficient than constructing a
2 dimensional matrix.    

## Constructing SNN graphs  

Since the adjacency matrix is symmetrical, we only need the computations for the upper triangle of the matrix. We iteratively compute the shared neighbors for each node, and then copy the result over to the other side. When parallelizing this, we only really need to be careful about where we overwrite cells in the array, so when using `# pragma omp parallel for` we are able to isolate each iteration in the outermost loop for each thread, which saves us from any possible race conditions.  


The algorithm for constructing a compressed snn adjacency matrix was a little more complex
given it's limitations. We construct an additional array which contains information about the size of each gap. This will allow us to better parallelize the for loop which increments the cells in the adjacency matrix.  


### Memory leak note:  

When running the openmp-parallelized versions for constructing the snn graphs,
valgrind seems to report a memory leak:

```
==4642== LEAK SUMMARY:
==4642==    definitely lost: 0 bytes in 0 blocks
==4642==    indirectly lost: 0 bytes in 0 blocks
==4642==      possibly lost: 2,016 bytes in 7 blocks
==4642==    still reachable: 3,344 bytes in 4 blocks
==4642==         suppressed: 0 bytes in 0 blocks
```

However, upon further investigation, it seems that this memory leak is not really
a problem after all, but rather a known issue between valgrind and openmp  
https://medium.com/@auraham/pseudo-memory-leaks-when-using-openmp-11a383cc4cf9  


## Graph clustering  

Lastly, the graph clustering algorithm implemented in the procedure `check_node` is a tree-recursive procedure, which initiates a lookup table for visited nodes when executing a depth-first search. It doesnt return anything, but instead outputs the cluster members to `stdout`. The id of the node checked is printed regardless of whether or not it belongs to a cluster.  
