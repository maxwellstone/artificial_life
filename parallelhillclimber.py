import copy
import numpy as np

from solution import Solution

import constants as c

class ParallelHillClimber:
    def __init__(self, id: str):
        self.id = id
        self.parents = [Solution(str(i)) for i in range(c.POPULATION_COUNT)]
        self.fitnesses = np.zeros(c.GENERATION_COUNT)

    def evolve(self):
        # First generation
        for parent in self.parents:
            parent.simulate(False)

        for parent in self.parents:
            parent.evaluate()

        for i in range(c.GENERATION_COUNT):
            print("Generation " + str(i) + "/" + str(c.GENERATION_COUNT))
            print("")

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
            for j in range(c.POPULATION_COUNT):
                child = children[j]
                parent = self.parents[j]

                print(str(j) + ": " + str(parent.fitness) + " | " + str(child.fitness))

                # Pick most fit
                if(child.fitness > parent.fitness):
                    self.parents[j] = child
            print("")

            # Track most fit
            self.fitnesses[i] = max(self.parents, key = lambda parent: parent.fitness).fitness

        best = max(self.parents, key = lambda parent: parent.fitness)
        print("Best: " + str(best.fitness) + "\n")
        best.simulate(True)
        best.evaluate()

        # Save a copy of the best body and brain
        best.save_body("body_evolved_" + self.id + ".urdf")
        best.save_brain("brain_evolved_" + self.id + ".nndf")

        # Save fitnesses
        np.save("fitnesses_" + self.id + ".npy", self.fitnesses)