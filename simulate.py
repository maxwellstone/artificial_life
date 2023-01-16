import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import time
import numpy
import random

amplitudeBackLeg = numpy.pi / 4
frequencyBackLeg = 10
phaseOffsetBackLeg = -numpy.pi / 8
amplitudeFrontLeg = numpy.pi / 8
frequencyFrontLeg = 10
phaseOffsetFrontLeg = 0

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

    targetAnglesBackLeg = amplitudeBackLeg * numpy.sin(frequencyBackLeg * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffsetBackLeg)
    targetAnglesFrontLeg = amplitudeFrontLeg * numpy.sin(frequencyFrontLeg * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffsetFrontLeg)

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAnglesBackLeg[i],
        maxForce = 20
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAnglesFrontLeg[i],
        maxForce = 20
    )

    time.sleep(1 / 1000)

p.disconnect()

numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)