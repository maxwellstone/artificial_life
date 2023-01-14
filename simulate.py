import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import time
import numpy

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

for i in range(1000):
    p.stepSimulation()

    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    time.sleep(1 / 60)

p.disconnect()

numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)