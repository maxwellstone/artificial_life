import pyrosim.pyrosim as pyrosim
import random

def create_world():
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name = "Box", pos = [-0.5, 0, 0.1], size = [0.3, 0.4, 0.2])

    pyrosim.End()

create_world()