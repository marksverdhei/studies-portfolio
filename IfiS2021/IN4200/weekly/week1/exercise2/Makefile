CC=gcc
CFLAGS=-std=gnu11 -g -Wunused
default: all

all: task1 task2

task1: task1.c
	$(CC) $(CFLAGS) task1.c -o task1 -lm

task2: task2.c
	$(CC) $(CFLAGS) task2.c -o task2 -lm

clean:
	$(RM) *.o
	$(RM) *.output
