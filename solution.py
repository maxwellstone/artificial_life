import pyrosim.pyrosim as pr
import numpy as np
import random
import time
import os

import constants as c

class Solution:
    def __init__(self, id: int):
        self.id = id
        self.weights = np.random.rand(c.SENSOR_NEURON_COUNT, c.MOTOR_NEURON_COUNT) * 2 - 1
        self.fitness = 0

    def simulate(self, show: bool):
        self.create_body("body.urdf", [0, 0, 1])
        self.create_brain("brain" + str(self.id) + ".nndf")

        os.system(("" if show else "start /B ") + "python simulate.py " + ("GUI" if show else "DIRECT") + " " + str(self.id))

    def evaluate(self):
        fitness_file = "fitness" + str(self.id) + ".txt"
        
        while not os.path.exists(fitness_file):
            time.sleep(0.01)

        try:
            file = open(fitness_file, "r")
            self.fitness = float(file.read())

            file.close()
        except:
            pass

        # Clean up files
        os.remove("brain" + str(self.id) + ".nndf")
        os.remove(fitness_file)

    def mutate(self):
        i = random.randint(0, c.SENSOR_NEURON_COUNT - 1)
        j = random.randint(0, c.MOTOR_NEURON_COUNT - 1)
        self.weights[i][j] = random.random() * 2 - 1

    def create_body(self, filename: str, pos: list[float]):
        pr.Start_URDF(filename)

        pr.Send_Cube(name = "A", pos = pos, size = [1, 1, 1])

        pr.Send_Joint(name = "A_B1", parent = "A", child = "B1", type = "revolute", position = [pos[0], pos[1] - 0.5, pos[2]], joint_axis = "0 1 0")
        pr.Send_Cube(name = "B1", pos = [0, -0.5, 0], size = [0.2, 1, 0.2])
        pr.Send_Joint(name = "B1_B2", parent = "B1", child = "B2", type = "revolute", position = [0, -1, 0], joint_axis = "1 0 0")
        pr.Send_Cube(name = "B2", pos = [0, 0, -0.5], size = [0.2, 0.2, 1])
        
        pr.Send_Joint(name = "A_C1", parent = "A", child = "C1", type = "revolute", position = [pos[0], pos[1] + 0.5, pos[2]], joint_axis = "0 1 0")
        pr.Send_Cube(name = "C1", pos = [0, 0.5, 0], size = [0.2, 1, 0.2])
        pr.Send_Joint(name = "C1_C2", parent = "C1", child = "C2", type = "revolute", position = [0, 1, 0], joint_axis = "1 0 0")
        pr.Send_Cube(name = "C2", pos = [0, 0, -0.5], size = [0.2, 0.2, 1])

        pr.Send_Joint(name = "A_D", parent = "A", child = "D", type = "revolute", position = [pos[0], pos[1], pos[2] - 0.5], joint_axis = "0 1 0")
        pr.Send_Cube(name = "D", pos = [0, 0, -0.25], size = [0.2, 0.2, 0.5])

        pr.End()

    def create_brain(self, filename: str):
        pr.Start_NeuralNetwork(filename)

        pr.Send_Sensor_Neuron(name = 0, linkName = "A")
        pr.Send_Sensor_Neuron(name = 1, linkName = "B1")
        pr.Send_Sensor_Neuron(name = 2, linkName = "B2")
        pr.Send_Sensor_Neuron(name = 3, linkName = "C1")
        pr.Send_Sensor_Neuron(name = 4, linkName = "C2")
        pr.Send_Sensor_Neuron(name = 5, linkName = "D")

        pr.Send_Motor_Neuron(name = 6, jointName = "A_B1")
        pr.Send_Motor_Neuron(name = 7, jointName = "B1_B2")
        pr.Send_Motor_Neuron(name = 8, jointName = "A_C1")
        pr.Send_Motor_Neuron(name = 9, jointName = "C1_C2")
        pr.Send_Motor_Neuron(name = 10, jointName = "A_D")

        for i in range(c.SENSOR_NEURON_COUNT):
            for j in range(c.MOTOR_NEURON_COUNT):
                pr.Send_Synapse(sourceNeuronName = i, targetNeuronName = c.SENSOR_NEURON_COUNT + j, weight = self.weights[i][j])

        pr.End()