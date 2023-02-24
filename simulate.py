import sys

from simulation import Simulation

mode_arg = sys.argv[1] if len(sys.argv) > 1 else "DIRECT"
id_arg = sys.argv[2] if len(sys.argv) > 2 else 0

simulation = Simulation(mode_arg, id_arg)
simulation.run()