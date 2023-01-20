import copy

from solution import Solution

import constants as c

class HillClimber:
    def __init__(self):
        self.soln = Solution()

    def evolve(self):
        self.soln.evaluate(True)
        for i in range(c.GENERATION_COUNT):
            # Spawn new child
            child = copy.deepcopy(self.soln)

            # Mutate child
            child.mutate()

            child.evaluate()
            print("\n" + str(self.soln.fitness) + " | " + str(child.fitness))

            # Pick the most fit
            if(child.fitness < self.soln.fitness):
                self.soln = child

        # Show final generation
        self.soln.evaluate(True)
