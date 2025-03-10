
# Running the programs  

This delivery contains a Makefile that serves as an interface for compiling
and running the programs. The programs themselves don't take any arguments,
but only test_snn.c has a main procedure.  

To compile and run the test program
```
make test
```  
or with valgrind:  
```
make test_memcheck
```

All library code is found in src:
`snn.c snn.h utils.c utils.h`  

the test program is in the test folder  

and the binaries are compiled and sent to the bin folder  

See the Makefile if details is necessary. The programs are compiled with GCC gnu11  
