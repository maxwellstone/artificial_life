import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")

matplotlib.pyplot.plot(backLegSensorValues, linewidth = 3)
matplotlib.pyplot.plot(frontLegSensorValues)

matplotlib.pyplot.legend(["Back Leg", "Front Leg"])

matplotlib.pyplot.show()