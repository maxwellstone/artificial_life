import pyrosim.pyrosim as pr
import numpy as np

import constants as c

class Sensor:
    def __init__(self, name: str):
        self.name = name
        self.values = np.zeros(c.MAX_STEPS)

    def update(self, step: int):
        self.values[step] = pr.Get_Touch_Sensor_Value_For_Link(self.name)

    def save(self):
        np.save("data/sensor_" + self.name + ".npy", self.values)