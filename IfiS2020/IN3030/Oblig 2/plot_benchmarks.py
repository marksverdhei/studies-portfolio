import numpy as np
import matplotlib.pyplot as plt

infile = open("speedups.txt", "r")
timings = next(infile)
timings = np.array([float(i) for i in timings.split()])
print(timings)
timings = timings.reshape((4, 3)).T
print(timings)

x_data = [100, 200, 500, 1000]
plt.title("Speedups")
plt.plot(x_data, timings[0], label="no transpose")
plt.plot(x_data, timings[1], label="b transposed")
plt.plot(x_data, timings[2], label="a transposed")

plt.scatter(x_data, timings[0])
plt.scatter(x_data, timings[1])
plt.scatter(x_data, timings[2])
plt.grid()
plt.legend()
# plt.show()
plt.savefig("speedups.png")
