import pyrosim.pyrosim as pr
import numpy as np
import random
import time
import os

from part import Part
from joint import Joint

import constants as c

class Solution:
    def __init__(self, id: int):
        self.id = id
        self.fitness = 0

        # Body
        self.parts = []
        self.joints = []
        self.sensors = [] # part indices
        
        part_count = random.randint(10, 15)
        root_pos = [0, 0, 2.0]
        self.parts.append(Part("root", root_pos, root_pos, (np.random.rand(3) + 1) * 0.5, bool(random.randint(0, 1))))
        for i in range(1, part_count):
            # Keep trying until we find a suitable attachment site
            while True:
                # Pick a random branch point
                parent = random.choice(self.parts)

                # Pick random branch direction
                dir = np.zeros(3)
                dir[random.randint(0, 2)] = random.choice([-1, 1])

                # Created randomized child
                size = (np.random.rand(3) + 1) * 0.5
                world_pos = parent.world_pos + dir * ((parent.size + size) / 2)
                child = Part(str(i), world_pos, dir * size / 2, size, bool(random.randint(0, 1)))

                # Check if the child intersects the floor or other parts
                if world_pos[2] - size[2] >= 0 and not any(child.intersects(part) for part in self.parts):
                    # Connect child
                    self.parts.append(child)
                    self.joints.append(Joint(parent, child, parent.pos + dir * parent.size / 2, random.choice([Joint.AXIS_X, Joint.AXIS_Y, Joint.AXIS_Z])))

                    break

        for i in range(len(self.parts)):
            if self.parts[i].sensor:
                self.sensors.append(i)

        # Brain
        self.weights = np.random.rand(len(self.sensors), len(self.joints)) * 2 - 1

    def simulate(self, show: bool):
        self.create_body("body" + str(self.id) + ".urdf")
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
        os.remove("body" + str(self.id) + ".urdf")
        os.remove("brain" + str(self.id) + ".nndf")
        os.remove(fitness_file)

    def mutate(self):
        i = random.randint(0, len(self.sensors) - 1)
        j = random.randint(0, len(self.joints) - 1)
        self.weights[i][j] = random.random() * 2 - 1

    def create_body(self, filename: str):
        pr.Start_URDF(filename)

        # Add parts
        for part in self.parts:
            color = [0, 1, 0, 1] if part.sensor else [0, 0, 1, 1]
            pr.Send_Cube(name = part.name, pos = part.pos, size = part.size, rgba = color)

        # Add joints
        for i in range(len(self.joints)):
            joint = self.joints[i]
            
            match joint.axis:
                case Joint.AXIS_X:
                    axis = "1 0 0"
                case Joint.AXIS_Y:
                    axis = "0 1 0"
                case Joint.AXIS_Z:
                    axis = "0 0 1"
            
            pr.Send_Joint(name = joint.parent.name + "_" + joint.child.name, parent = joint.parent.name, child = joint.child.name, type = "revolute", position = joint.pos, joint_axis = axis)

        pr.End()

    def create_brain(self, filename: str):
        pr.Start_NeuralNetwork(filename)

        # Add sensors
        for i in range(len(self.sensors)):
            pr.Send_Sensor_Neuron(name = i, linkName = self.parts[self.sensors[i]].name)

        # Add motors
        for i in range(len(self.joints)):
            joint = self.joints[i]
            pr.Send_Motor_Neuron(name = len(self.sensors) + i, jointName = joint.parent.name + "_" + joint.child.name)

        # Add weights
        for i in range(len(self.sensors)):
            for j in range(len(self.joints)):
                pr.Send_Synapse(sourceNeuronName = i, targetNeuronName = len(self.sensors) + j, weight = self.weights[i][j])

        pr.End()