import sys

from simulation import Simulation

mode_arg = sys.argv[1] if len(sys.argv) > 1 else "DIRECT"
time_arg = sys.argv[2] if len(sys.argv) > 2 else "n"
simulation = Simulation(mode_arg, time_arg)
simulation.run()