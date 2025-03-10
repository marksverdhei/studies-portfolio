import matplotlib.pyplot as plt
import numpy as np
import os
from sys import argv
t = None
if len(argv) > 1:
    t = int(argv[1])

def make_plots(ns, seq_times, para_times, speedups):
    fig, ax = plt.subplots()
    ax.set_title("Radix sort benchmarks")
    ax.scatter(ns, seq_times, c="blue")
    ax.scatter(ns, para_times, c="orange")
    ax.plot(ns, seq_times, label="sequential", c="blue")
    ax.plot(ns, para_times, label="parallel", c="orange")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("median ms")
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
    seq_times = np.array(seq_times, dtype="int", copy=True)
    para_times = np.array(para_times, dtype="int", copy=True)
    table_lines = ["|n|sequential|parallel|speedup|  \n",
                   "|:-:|:-:|:-:|:-:|  \n"]

    table_lines += [f"|{ns[i]}|{seq_times[i]}ms|{para_times[i]}ms|{round(speedups[i], 3)}|  \n" for i in range(len(ns))]
    return table_lines

if t is None:
    os.system("java Speedup --full --toFile")
else:
    os.system(f"java Speedup --full --toFile t={t}")

data = np.genfromtxt("speedups.txt", delimiter=",")
ns, seq_times, para_times, speedups = data.T
make_plots(ns, seq_times, para_times, speedups)
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
os.system("pandoc report2.md -o report.pdf")
