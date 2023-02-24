import os

from solution import Solution

s = Solution("unevolved")
s.simulate(True)
s.evaluate()

os.system("python simulate.py GUI _evolved_5")
os.remove("fitness_evolved_5.txt")