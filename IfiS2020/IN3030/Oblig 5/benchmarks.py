import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--full", action="store_true")
    parser.add_argument("-b", "--benchmark", action="store_true")
    parser.add_argument("-p", "--plot", action="store_true")
    parser.add_argument("-t", "--table", action="store_true")
    parser.add_argument("-r", "--recompile", action="store_true")
    return parser.parse_args()


def si_unit(t: float):

    if t > 10 ** 9:
        return f"{round(t/(10**9), 2)}s"
    elif t > 10 ** 4:
        return f"{round(t/(10**6), 2)}ms"
    else:
        return f"{t}ns"

def make_plots(ns, seq_times, para_times, speedups):
    fig, ax = plt.subplots()
    ax.set_title("Convex hull benchmarks")
    ax.scatter(ns, seq_times, c="blue")
    ax.scatter(ns, para_times, c="orange")
    ax.plot(ns, seq_times, label="sequential", c="blue")
    ax.plot(ns, para_times, label="parallel", c="orange")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("median (ns)")
    ax.set_xlabel("input size")

    ax.grid()
    ax.legend()
    plt.savefig("timings.png")
    plt.show()

    a = np.ones(ns.shape)
    fig, ax = plt.subplots()
    ax.set_title("Speedup")
    ax.plot(ns, a, color="blue", alpha=0.4)
    ax.plot(ns, speedups, c="orange")
    ax.scatter(ns, speedups, c="orange", label="speedup")
    ax.set_xscale("log")
    ax.set_xlabel("input size")
    ax.set_ylabel("speedup")
    ax.grid()
    ax.legend()
    plt.savefig("speedups.png")
    plt.show()

def make_table(ns, seq_times, para_times, speedups):
    ns = np.array(ns, dtype="int", copy=True)
    seq_times_si = [si_unit(i) for i in seq_times]
    para_times_si = [si_unit(i) for i in para_times]
    table_lines = ["|n|sequential|parallel|speedup|  \n",
                   "|:-:|:-:|:-:|:-:|  \n"]

    table_lines += [f"|{ns[i]}|{seq_times_si[i]}|{para_times_si[i]}|{round(speedups[i], 3)}|  \n" for i in range(len(ns))]
    return table_lines


if __name__ == "__main__":
    args = parse_args()

    if args.full:
        args.benchmark = True
        args.plot = True
        args.table = True

    if args.table:
        args.recompile = True

    if args.benchmark: os.system("java -Xmx6000m Speedup --full --toFile")

    data = np.genfromtxt("speedups.txt", delimiter=",")
    ns, seq_times, para_times, speedups = data.T

    if args.plot: make_plots(ns, seq_times, para_times, speedups)

    if args.table:
        table_lines = make_table(ns, seq_times, para_times, speedups)
        with open("report.md") as src:
            lines = src.readlines()

        with open("report2.md", "w+") as dst:
            start = None
            for i, line in enumerate(lines):
                if line.startswith("## Measurements"):
                    start = i
                if start is not None:
                    if line.startswith("!"):
                        end = i
                        break
            new_lines = lines[:start+1] + table_lines + lines[end:]
            dst.write("".join(new_lines))

    if args.recompile:
        os.system("pandoc report2.md -o report.pdf")
