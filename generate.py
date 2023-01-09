import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

x = 0
y = 0
z = 0.5
length = 1
width = 1
height = 1

for i in range(5):
    for j in range(5):
        scale = 1
        for k in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x - 2.5 + i, y - 2.5 + j, z + k], size=[length * scale, width * scale, height * scale])
            scale *= 0.9

pyrosim.End()