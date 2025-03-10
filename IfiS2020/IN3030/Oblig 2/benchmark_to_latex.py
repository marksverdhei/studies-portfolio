from functools import reduce
from operator import concat

def transpose_file():
    fin = open("benchmarks.txt", "r")
    out = open("latex_tables.txt", "w+")

    out.write("\n".join(map(lambda x: " ".join(x),
        zip(*map(lambda x: x.strip().split(","), fin)))))

def wite_tables():
    fin = open("benchmarks.txt", "r")
    out = open("latex_tables2.txt", "w+")

    m = map(si_unit,
            map(lambda x: x[5:],
                filter(lambda x: x.startswith("time="),
                    reduce(concat,
                        map(lambda x: x.strip().split(", "), fin)))))
    l = list(m)

    l[::6] = list(map(lambda x: r" \hline \\ \hline 100 & " + x , l[::6]))

    print(l)

    s = " & ".join(l[6::])
    print(s)
    out.write(s)

def si_unit(s):
    try:
        t = int(s)
    except:
        return "n/a"

    if t > 10 ** 9:
        return f"{round(t/(10**9), 2)}s"
    elif t > 10 ** 6:
        return f"{round(t/(10**6), 2)}ms"
    else:
        return s+"ns"

def write_speedups():
    fin = open("latex_tables.txt", "r")
    out = open("speedups.txt", "w+")

    r = list(map(lambda x: int(x[5:]), filter(lambda x: x.startswith("time="), fin.read().split())))
    z = map(lambda x, y: str(round(x / y, 2)), r[::2], r[1::2])
    out.write(" ".join(z))


transpose_file()
write_speedups()
