import numpy as np
import matplotlib.pyplot as plt

fitnesses = [np.load("fitnesses_" + str(i + 1) + ".npy") for i in range(10)]

plt.title("Overall Fitness")
plt.xlabel("Generations")
plt.ylabel("Fitness")

for i in range(10):
    plt.plot(fitnesses[i], label = "Seed " + str(i + 1))
plt.legend(fontsize = "x-small")

plt.show()

for i in range(10):
    plt.title("Seed " + str(i + 1) + " Fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")

    plt.plot(fitnesses[i])

    plt.show()