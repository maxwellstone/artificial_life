import pyrosim.pyrosim as pr
import numpy as np
import random
import time
import os

class Solution:
    def __init__(self, id: int):
        self.id = id
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.fitness = 0

    def simulate(self, show: bool):
        self.create_brain("brain" + str(self.id) + ".nndf")

        os.system(("" if show else "start /B ") + "python simulate.py " + ("GUI" if show else "DIRECT") + " " + str(self.id))

    def evaluate(self):
        fitness_file = "fitness" + str(self.id) + ".txt"
        
        while not os.path.exists(fitness_file):
            time.sleep(0.01)

        file = open(fitness_file, "r")
        try:
            self.fitness = float(file.read())
        except:
            pass
        file.close()

        # Clean up files
        os.remove("brain" + str(self.id) + ".nndf")
        os.remove(fitness_file)

    def mutate(self):
        i = random.randint(0, 2)
        j = random.randint(0, 1)
        self.weights[i][j] = random.random() * 2 - 1

    def create_body(self, filename: str):
        pr.Start_URDF(filename)

        pr.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1, 1, 1])
        pr.Send_Joint(name="Torso_BackLeg", parent="Torso", child ="BackLeg", type="revolute", position=[1, 0, 1])
        pr.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pr.Send_Joint(name="Torso_FrontLeg", parent="Torso", child ="FrontLeg", type="revolute", position=[2, 0, 1])
        pr.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])

        pr.End()

    def create_brain(self, filename: str):
        pr.Start_NeuralNetwork(filename)

        pr.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pr.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pr.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

        pr.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
        pr.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")

        for i in range(3):
            for j in range(2):
                pr.Send_Synapse(sourceNeuronName = i, targetNeuronName = 3 + j, weight = self.weights[i][j])

        pr.End()