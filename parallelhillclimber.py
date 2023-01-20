import copy

from solution import Solution

import constants as c

class ParallelHillClimber:
    def __init__(self):
        self.parents = [Solution(i) for i in range(c.POPULATION_COUNT)]

    def evolve(self):
        # First generation
        for parent in self.parents:
            parent.simulate(False)

        for parent in self.parents:
            parent.evaluate()

        for i in range(c.GENERATION_COUNT):
            # Spawn new children
            children = [copy.deepcopy(parent) for parent in self.parents]

            # Mutate children
            for child in children:
                child.mutate()
                child.simulate(False)

            for child in children:
                child.evaluate()

            # Printing and selection
            print("\n")
            for i in range(c.POPULATION_COUNT):
                child = children[i]
                parent = self.parents[i]

                print(str(i) + ": " + str(parent.fitness) + " | " + str(child.fitness))

                # Pick most fit
                if(child.fitness < parent.fitness):
                    self.parents[i] = child
            print("")

        best = min(self.parents, key = lambda parent: parent.fitness)
        print("Best: " + str(best.fitness) + "\n")
        best.simulate(True)