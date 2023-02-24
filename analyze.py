import numpy as np
import matplotlib.pyplot as plt

fitnesses = [np.load("fitnesses_" + str(i + 1) + ".npy") for i in range(5)]

for i in range(5):
    plt.title("Seed " + str(i + 1) + " Fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")

    plt.plot(fitnesses[i])

    plt.show()