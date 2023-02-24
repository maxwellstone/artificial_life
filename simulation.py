import pybullet as pb
import pybullet_data
import time
import os

import constants as c

from world import World
from robot import Robot

class Simulation:
    def __init__(self, mode_arg: str, id_arg: str):
        self.mode = pb.DIRECT
        if mode_arg == "GUI":
            self.mode = pb.GUI
        
        self.soln_id = id_arg

        # Start pybullet
        pb.connect(self.mode)
        pb.setAdditionalSearchPath(pybullet_data.getDataPath())
        if self.mode == pb.GUI:
            pb.configureDebugVisualizer(pb.COV_ENABLE_GUI,0)

        # Set scene forces
        pb.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)

        # Create scene
        self.world = World()
        self.robot = Robot("body" + self.soln_id + ".urdf", "brain" + self.soln_id + ".nndf")

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

            # Try to get each frame to take the same amount of time
            # if self.mode == pb.GUI:
            #     time.sleep(max(c.FRAME_TIME - (time.time() - time_start), 0))

            step += 1
        
        # Write fitness to file
        if(pb.getConnectionInfo()['isConnected']):
            file = open("tmp_fitness" + self.soln_id + ".txt", "w")
            file.write(str(self.robot.fitness()))
            file.close()
            os.rename("tmp_fitness" + self.soln_id + ".txt", "fitness" + self.soln_id + ".txt")