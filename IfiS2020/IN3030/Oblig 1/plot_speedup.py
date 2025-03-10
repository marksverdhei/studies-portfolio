import matplotlib.pyplot as plt
import numpy as np
benchmarks = open("benchmarks.csv")

n_values = []
k_20 = []
k_100 = []

for line in benchmarks:
    if line.startswith("n"):
        n_values.append(int(line.split(" ")[2]))
    elif line.startswith("k = 20"):
        stats = next(benchmarks)
        k_20.append([int(i) for i in stats.split(",") if i.isdigit()])
    elif line.startswith("k = 100"):
        stats = next(benchmarks)
        k_100.append([int(i) for i in stats.split(",") if i.isdigit()])


n_values = np.array(n_values, dtype="uint64")
k_20 = np.array(k_20, dtype="uint64").T
k_100 = np.array(k_100, dtype="uint64").T

#
# fig = plt.Figure()
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)
def plot_runtimes_etc():
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,2,3)
    ax4 = plt.subplot(2,2,4)

    axn = [ax1, ax2, ax3, ax4]

    for ax_times, ax_speedup, k_n in [(ax1, ax2, k_20), (ax3, ax4, k_100)]:
        ax_times.plot(n_values, k_n[1], label="a2 sequential")

        for i in range(2, k_n.shape[0]):
            ax_times.plot(n_values, k_n[i], label=f"t = {2**(i-1)}")

        ax_times.set_xscale("log")
        ax_times.set_yscale("log")

        ax_speedup.plot(n_values, k_n[1]/k_n[1], label="a2 sequential")

        for i in range(2, k_n.shape[0]):
            ax_speedup.plot(n_values, k_n[1]/k_n[i], label=f"t = {2**(i-1)}")

        ax_speedup.set_xscale("log")

    for ax in axn:
        ax.grid()
        ax.legend()

fig1 = plt.Figure()

ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_xscale("log")
# ax1.set_yscale("log")

ax1.plot(n_values, k_20[0]/k_20[1], label="k=20")
ax1.plot(n_values, k_100[0]/k_100[1], label="k=100")
ax1.grid()
ax1.legend()
ax1.set_title("speedup on a1 vs a2 sequential")
ax1.set_ylabel("Speedup")
ax1.set_xlabel("Array size")

fig2 = plt.Figure()

ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_xscale("log")
ax2.plot(n_values, k_20[1]/k_20[3], label="k=20")
ax2.plot(n_values, k_100[1]/k_100[3], label="k=100")
ax2.grid()
ax2.legend()
ax2.set_title("speedup on a2 sequential vs parallel (t = 4)")
ax2.set_ylabel("Speedup")
ax2.set_xlabel("Array size")
# plot_runtimes_etc()

fig1.savefig("speedup_sequential.png")

fig2.savefig("speedup_parallel.png")
