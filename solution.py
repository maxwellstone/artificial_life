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
        self.create_body("body.urdf")
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
        i = random.randint(0, c.SENSOR_NEURON_COUNT - 1)
        j = random.randint(0, c.MOTOR_NEURON_COUNT - 1)
        self.weights[i][j] = random.random() * 2 - 1

    def create_body(self, filename: str):
        pr.Start_URDF(filename)

        pr.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])

        pr.Send_Joint(name="Torso_BackLeg", parent="Torso", child ="BackLeg", type="revolute", position=[0, -0.5, 1], joint_axis = "1 0 0")
        pr.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pr.Send_Joint(name="BackLeg_LBL", parent="BackLeg", child ="LBL", type="revolute", position=[0, -1, 0], joint_axis = "1 0 0")
        pr.Send_Cube(name="LBL", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        
        pr.Send_Joint(name="Torso_FrontLeg", parent="Torso", child ="FrontLeg", type="revolute", position=[0, 0.5, 1], joint_axis = "1 0 0")
        pr.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pr.Send_Joint(name="FrontLeg_LFL", parent="FrontLeg", child ="LFL", type="revolute", position=[0, 1, 0], joint_axis = "1 0 0")
        pr.Send_Cube(name="LFL", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        
        pr.Send_Joint(name="Torso_LeftLeg", parent="Torso", child ="LeftLeg", type="revolute", position=[-0.5, 0, 1], joint_axis = "0 1 0")
        pr.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        pr.Send_Joint(name="LeftLeg_LLL", parent="LeftLeg", child ="LLL", type="revolute", position=[-1, 0, 0], joint_axis = "0 1 0")
        pr.Send_Cube(name="LLL", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        
        pr.Send_Joint(name="Torso_RightLeg", parent="Torso", child ="RightLeg", type="revolute", position=[0.5, 0, 1], joint_axis = "0 1 0")
        pr.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        pr.Send_Joint(name="RightLeg_LRL", parent="RightLeg", child ="LRL", type="revolute", position=[1, 0, 0], joint_axis = "0, 1 0")
        pr.Send_Cube(name="LRL", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pr.End()

    def create_brain(self, filename: str):
        pr.Start_NeuralNetwork(filename)

        pr.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pr.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pr.Send_Sensor_Neuron(name = 2, linkName = "LBL")
        pr.Send_Sensor_Neuron(name = 3, linkName = "FrontLeg")
        pr.Send_Sensor_Neuron(name = 4, linkName = "LFL")
        pr.Send_Sensor_Neuron(name = 5, linkName = "LeftLeg")
        pr.Send_Sensor_Neuron(name = 6, linkName = "LLL")
        pr.Send_Sensor_Neuron(name = 7, linkName = "RightLeg")
        pr.Send_Sensor_Neuron(name = 8, linkName = "LRL")

        pr.Send_Motor_Neuron(name = 9, jointName = "Torso_BackLeg")
        pr.Send_Motor_Neuron(name = 10, jointName = "BackLeg_LBL")
        pr.Send_Motor_Neuron(name = 11, jointName = "Torso_FrontLeg")
        pr.Send_Motor_Neuron(name = 12, jointName = "FrontLeg_LFL")
        pr.Send_Motor_Neuron(name = 13, jointName = "Torso_LeftLeg")
        pr.Send_Motor_Neuron(name = 14, jointName = "LeftLeg_LLL")
        pr.Send_Motor_Neuron(name = 15, jointName = "Torso_RightLeg")
        pr.Send_Motor_Neuron(name = 16, jointName = "RightLeg_LRL")

        for i in range(c.SENSOR_NEURON_COUNT):
            for j in range(c.MOTOR_NEURON_COUNT):
                pr.Send_Synapse(sourceNeuronName = i, targetNeuronName = c.SENSOR_NEURON_COUNT + j, weight = self.weights[i][j])

        pr.End()