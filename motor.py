import pyrosim.pyrosim as pr
import pybullet as pb
import numpy as np

import constants as c

import robot as Robot

class Motor:
    def __init__(self, robot: Robot, name: bytes):
        self.robot = robot
        self.name = name

    def update(self, angle: float):
        pr.Set_Motor_For_Joint(
            bodyIndex = self.robot.id,
            jointName = self.name,
            controlMode = pb.POSITION_CONTROL,
            targetPosition = angle,
            maxForce = c.LEG_STRENGTH
        )