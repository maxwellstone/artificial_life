import os

from parallelhillclimber import ParallelHillClimber

# Make sure no files were left over
os.system("del fitness*.txt")
os.system("del tmp_fitness*.txt")
os.system("del brain*.nndf")

hc = ParallelHillClimber()
hc.evolve()

# Make sure no files were left over
os.system("del fitness*.txt")
os.system("del tmp_fitness*.txt")
os.system("del brain*.nndf")