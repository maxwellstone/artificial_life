import pyrosim.pyrosim as pr
import pybullet as pb
import numpy as np

import constants as c

import robot as Robot

class Motor:
    def __init__(self, robot: Robot, name: bytes):
        self.robot = robot
        self.name = name

        if self.name == b"Torso_BackLeg":
            self.amplitude = c.BACK_LEG_AMPLITUDE
            self.frequency = c.BACK_LEG_FREQUENCY
            self.phase = c.BACK_LEG_PHASE
        else:
            self.amplitude = c.FRONT_LEG_AMPLITUDE
            self.frequency = c.FRONT_LEG_FREQUENCY
            self.phase = c.FRONT_LEG_PHASE

        self.values = self.amplitude * np.sin(np.linspace(0, self.frequency * 2 * np.pi, c.MAX_STEPS) + self.phase)

    def update(self, step: int):
        pr.Set_Motor_For_Joint(
            bodyIndex = self.robot.id,
            jointName = self.name,
            controlMode = pb.POSITION_CONTROL,
            targetPosition = self.values[step],
            maxForce = c.LEG_STRENGTH
        )

    def save(self):
        np.save("data/motor_" + self.name.decode() + ".npy", self.values)