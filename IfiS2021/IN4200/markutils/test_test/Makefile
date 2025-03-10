
default: compile test

compile:
	gcc -c -fPIC foo.c -o foo.o
	gcc foo.o -shared -o foo.so

test:
	python3 test_foo.py
