JC = javac

default: compile

compile:
	$(JC) *.java

clean:
	$(RM) *.class

pdf:
	python3 benchmarks.py --table

benchmark:
	python3 benchmarks.py --full
