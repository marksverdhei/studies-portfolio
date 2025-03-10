import matplotlib.pyplot as plt
n_values = []
seq_sieve_times = []
para_sieve_times = []
prime_fac_times = []
para_fac_times = []
with open("measurements.txt", "r") as f:
    for line in f:
        tok = line.strip().split()
        if not tok:
            continue

        if tok[0] == "n":
            n_values.append(int(tok[2]))
        elif tok[0] == "sequentialSieve:":
            seq_sieve_times.append(int(tok[1]))
        elif tok[0] == "parallelSieve:":
            para_sieve_times.append(int(tok[1]))
        elif tok[0] == "sequential":
            prime_fac_times.append(int(tok[2]))
        elif tok[0] == "parallel":
            para_fac_times.append(int(tok[2]))

print(n_values)
print(seq_sieve_times)
print(para_sieve_times)
print(prime_fac_times)
print(para_fac_times)


fig, ax = plt.subplots()
ax.set_title("Timings for sieve of Erathostenes")
ax.set_xlabel("n")
ax.set_ylabel("nanoseconds")
ax.plot(n_values, seq_sieve_times, label="sequential")
ax.plot(n_values, para_sieve_times, label="parallel")
ax.grid()
ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")
plt.savefig("sieve_times2.png")
plt.show()

fig, ax = plt.subplots()
ax.set_title("Speedups for sieve of Erathostenes")
ax.plot(n_values, [s/p for s, p in zip(seq_sieve_times, para_sieve_times)], label="speedup")
ax.grid()
ax.set_xlabel("n")
ax.legend()
ax.set_xscale("log")
plt.savefig("sieve_speedups2.png")
plt.show()

fig, ax = plt.subplots()
ax.set_title("Timings for prime number factorization")
ax.plot(n_values, prime_fac_times, label="sequential")
ax.plot(n_values, para_fac_times, label="parallel")
ax.grid()
ax.set_xlabel("n")
ax.set_ylabel("nanoseconds")
ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")
plt.savefig("primefac_times2.png")
plt.show()

fig, ax = plt.subplots()
ax.set_title("Speedups for prime number factorization")
ax.plot(n_values, [s/p for s, p in zip(prime_fac_times, para_fac_times)], label="speedup")
ax.grid()
ax.set_xlabel("n")
ax.legend()
ax.set_xscale("log")
plt.savefig("primefac_speedups2.png")
plt.show()
