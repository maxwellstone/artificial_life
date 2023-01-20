import sys

from simulation import Simulation

mode_arg = sys.argv[1] if len(sys.argv) > 1 else "DIRECT"
simulation = Simulation(mode_arg)
simulation.run()