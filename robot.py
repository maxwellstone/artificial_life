import pybullet as pb
import pyrosim.pyrosim as pr
from pyrosim.neuralNetwork import NEURAL_NETWORK

from sensor import Sensor
from motor import Motor

import constants as c

class Robot:
    def __init__(self, body_file: str, brain_file: str):
        # Initialize the robot
        self.id = pb.loadURDF(body_file)
        pr.Prepare_To_Simulate(self.id)

        # Create sensors
        self.sensors = {}
        for name in pr.linkNamesToIndices:
            self.sensors[name] = Sensor(name)

        # Create motors
        self.motors = {}
        for name in pr.jointNamesToIndices:
            self.motors[name] = Motor(self, name)

        self.nn = NEURAL_NETWORK(brain_file)

    def update(self, step: int):
        # Update sensors
        for sensor in self.sensors.values():
            sensor.update(step)

        # Update NN
        self.nn.Update()

        # Update motors
        for n in self.nn.neurons.values():
            if n.Is_Motor_Neuron():
                self.motors[n.Get_Joint_Name().encode()].update(n.Get_Value() * c.JOINT_RANGE)

    def fitness(self) -> float:
        po = pb.getBasePositionAndOrientation(self.id)
        pos = po[0]
        # Squared distance
        return pos[0] * pos[0] + pos[1] * pos[1] + pos[2] * pos[2]

    def save(self):
        for sensor in self.sensors.values():
            sensor.save()