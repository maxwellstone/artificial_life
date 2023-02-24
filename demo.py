import os

from solution import Solution

s = Solution("unevolved")
s.simulate(True)
s.evaluate()

for i in range(5):
    os.system("python simulate.py GUI _evolved_" + str(i + 1))
    os.remove("fitness_evolved_" + str(i + 1) + ".txt")