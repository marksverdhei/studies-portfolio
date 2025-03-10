CC=gcc
# CC=g++

CFLAGS=-std=gnu11 -g -fopenmp

CANDIDATE_ID=15833

DELIVERY_FOLDER=IN4200_HE1_$(CANDIDATE_ID)

bin:
	-mkdir bin

utils: src/utils.c bin
	$(CC) $(CFLAG) -c src/utils.c -o bin/utils.o

snn: src/snn.c bin
	$(CC) $(CFLAGS) -c -fPIC src/snn.c -o bin/snn.o -lm

snnso: snn utils
	$(CC) $(CFLAGS) bin/snn.o bin/utils.o -shared -o bin/snn.so

compile_test: test/test_snn.c snn utils
	$(CC) $(CFLAGS) -c test/test_snn.c -o bin/test_snn.o
	$(CC) $(CFLAGS) bin/snn.o bin/utils.o bin/test_snn.o -o bin/test_snn

test: compile_test
	bin/test_snn

test_memcheck: compile_test
	valgrind --leak-check=full --show-leak-kinds=all bin/test_snn

clean_delivery:
	-rm $(DELIVERY_FOLDER).zip
	-rm -r delivery/

pdf:
	pandoc report.md -o report.pdf

delivery: clean_delivery pdf
	mkdir delivery
	mkdir delivery/bin
	mkdir delivery/data
	cp data/simple-graph.txt delivery/data/simple_graph.txt
	cp -r src delivery/src
	cp -r test/ delivery/test
	cp Makefile delivery/Makefile
	cp report.pdf delivery/
	cp README.md delivery/
	zip -r $(DELIVERY_FOLDER).zip delivery/
	# cp -r data/ delivery/data

clean:
	$(RM) *.o
	$(RM) *.so
	$(RM) *.output
