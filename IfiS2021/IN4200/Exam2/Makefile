
MPICC=/usr/lib64/openmpi/bin/mpicc
MPIRUN=/usr/lib64/openmpi/bin/mpirun

PROGRAM=task.c
dest?=task

compile:
	$(MPICC) $(PROGRAM) -o $(dest)

run:
	$(MPIRUN) $(dest)
