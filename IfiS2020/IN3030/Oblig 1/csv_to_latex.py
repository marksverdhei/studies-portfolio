
in_file = open("benchmarks.csv")
out_file = open("benchmark_tables.txt", "w+", encoding="UTF8")

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

out_file.write(r"\begin{tabular}{|c|c|c|c|c|c|c|c|}")

for line in in_file:
    if line.startswith("n"):
        out_file.write("\n")
        out_file.write(r"\hline ")
        out_file.write(r"\multicolumn{8}{|c|}{"+line+"} \\\\\n")
        out_file.write("\n")
        out_file.write(r"\hline ")
        out_file.write("\n")
        out_file.write(r"\hline k & a1 & a2s & a2p t = 2 & t = 4 & t = 8 & t = 16 & t = 32 \\")
        for i in range(2):
            out_file.write(r"\hline ")
            out_file.write(next(in_file))
            out_file.write(" & ")
            out_file.write(" & ".join(map(si_unit, next(in_file).split(","))).strip(" & \n")+"\n")

            out_file.write("\\\\\n")

out_file.write(r"\hline")
out_file.write(r"\end{tabular}")
