import os
import sys

from solution import Solution

def run(id: str):
    os.system("python simulate.py GUI " + id)
    try:
        os.remove("fitness" + id + ".txt")
    except:
        pass

if len(sys.argv) > 1:
    try:
        x = int(sys.argv[1])
        if x < 1 or x > 10:
            raise
    except:
        print("Valid id numbers are between 1 and 10")
    else:
        run("_evolved_" + sys.argv[1])
else:
    s = Solution("unevolved")
    s.simulate(True)
    s.evaluate()

    for i in range(10):
        run("_evolved_" + str(i + 1))