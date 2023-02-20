import pyrosim.pyrosim as pyrosim
import random

def create_world():
    pyrosim.Start_SDF("world.sdf")

    pyrosim.End()

create_world()