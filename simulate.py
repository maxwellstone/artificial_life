import sys

from simulation import Simulation

mode_arg = sys.argv[1] if len(sys.argv) > 1 else "DIRECT"

try:
    id_arg = int(sys.argv[2]) if len(sys.argv) > 1 else 0
except:
    id_arg = 0

simulation = Simulation(mode_arg, id_arg)
simulation.run()