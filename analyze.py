import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

plt.plot(backLegSensorValues, linewidth = 3)
plt.plot(frontLegSensorValues)

plt.legend(["Back Leg", "Front Leg"])

plt.show()