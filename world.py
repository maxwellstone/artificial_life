import pybullet as pb

class World:
    def __init__(self):
        pb.loadURDF("plane.urdf")
        pb.loadSDF("world.sdf")