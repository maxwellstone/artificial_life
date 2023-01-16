import pybullet as pb
import pyrosim.pyrosim as pr

from sensor import Sensor
from motor import Motor

class Robot:
    def __init__(self):
        # Initialize the robot
        self.id = pb.loadURDF("body.urdf")
        pr.Prepare_To_Simulate(self.id)

        # Create sensors
        self.sensors = {}
        for name in pr.linkNamesToIndices:
            self.sensors[name] = Sensor(name)

        # Create motors
        self.motors = {}
        for name in pr.jointNamesToIndices:
            self.motors[name] = Motor(self, name)

    def update(self, step: int):
        # Update sensors
        for sensor in self.sensors.values():
            sensor.update(step)

        # Update motors
        for motor in self.motors.values():
            motor.update(step)

    def save(self):
        for sensor in self.sensors.values():
            sensor.save()
        for motor in self.motors.values():
            motor.save()