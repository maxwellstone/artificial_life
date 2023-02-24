import os
import sys
import numpy as np
import random

from parallelhillclimber import ParallelHillClimber

seed = 0
if len(sys.argv) > 1:
    try:
        seed = int(sys.argv[1])
        np.random.seed(seed)
        random.seed(seed)
    except:
        pass

hc = ParallelHillClimber(str(seed))
hc.evolve()