import pybullet as pb
import pybullet_data
import time

import constants as c

from world import World
from robot import Robot

class Simulation:
    def __init__(self, mode_arg: str, time_arg: str):
        mode = pb.DIRECT
        if mode_arg == "GUI":
            mode = pb.GUI
        
        self.use_time = time_arg.startswith("y")

        # Start pybullet
        pb.connect(mode)
        pb.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Create scene
        self.world = World()
        self.robot = Robot()

        # Set scene forces
        pb.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)

    def __del__(self):
        if(pb.getConnectionInfo()['isConnected']):
            pb.disconnect()

    def run(self):
        # Loop until the client is closed or enough steps have passed
        step = 0
        while(pb.getConnectionInfo()['isConnected'] and step < c.MAX_STEPS):
            time_start = time.time()

            pb.stepSimulation()

            self.robot.update(step)

            self.fitness()

            # Try to get each frame to take the same amount of time
            if self.use_time:
                time.sleep(max(c.FRAME_TIME - (time.time() - time_start), 0))

            step += 1

    def fitness(self):
        file = open("fitness.txt", "w")
        file.write(str(self.robot.fitness()))
        file.close()