CC=gcc
CFLAGS=-std=gnu11 -g -Wunused
default: all

all: task1

task1: task1.c
	$(CC) $(CFLAGS) task1.c -o task1 -lm

clean:
	$(RM) *.o
	$(RM) *.output
