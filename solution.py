import pyrosim.pyrosim as pr
import numpy as np
import random

import os

class Solution:
    def __init__(self):
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.fitness = 0

    def evaluate(self, show: bool = False):
        self.create_world()
        self.create_body()
        self.create_brain()

        os.system("python simulate.py " + ("GUI" if show else "DIRECT"))

        file = open("fitness.txt", "r")
        self.fitness = float(file.read())
        file.close()

    def mutate(self):
        i = random.randint(0, 2)
        j = random.randint(0, 1)
        self.weights[i][j] = random.random() * 2 - 1

    def create_world(self):
        pr.Start_SDF("world.sdf")

        pr.Send_Cube(name="Box", pos=[-3, 3, 0.5], size=[1, 1, 1])

        pr.End()

    def create_body(self):
        pr.Start_URDF("body.urdf")

        pr.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1, 1, 1])
        pr.Send_Joint(name="Torso_BackLeg", parent="Torso", child ="BackLeg", type="revolute", position=[1, 0, 1])
        pr.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pr.Send_Joint(name="Torso_FrontLeg", parent="Torso", child ="FrontLeg", type="revolute", position=[2, 0, 1])
        pr.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])

        pr.End()

    def create_brain(self):
        pr.Start_NeuralNetwork("brain.nndf")

        pr.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pr.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pr.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

        pr.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
        pr.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")

        for i in range(3):
            for j in range(2):
                pr.Send_Synapse(sourceNeuronName = i, targetNeuronName = 3 + j, weight = self.weights[i][j])

        pr.End()