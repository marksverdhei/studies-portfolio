
in_file = open("benchmarks.csv")
out_file = open("benchmark_tables2.txt", "w+", encoding="UTF8")

table1 = []
table2 = []

add_tables = lambda x : (table1.append(x), table2.append(x))

def si_unit(s):
    try:
        t = int(s)
    except:
        return ""

    if t > 10 ** 9:
        return f"{round(t/(10**9), 2)}s"
    elif t > 10 ** 6:
        return f"{round(t/(10**6), 2)}ms"
    else:
        return s+"ns"

add_tables(r"\begin{tabular}{|c|c|c|c|c|c|c|c|}")
add_tables(r"\hline n & a1 & a2s & a2p t = 2 & t = 4 & t = 8 & t = 16 & t = 32 \\ \hline")

for line in in_file:
    if line.startswith("n"):
        add_tables("\n")
        for table in [table1, table2]:
            next(in_file)

            table.append(line+" & "+(" & ".join(map(si_unit, next(in_file).split(","))).strip().strip("&")))

            table.append("\\\\\n")
            table.append(r"\hline ")

add_tables(r"\end{tabular}")

out_file.write(" ".join(table1 + table2))
