import pylab
import radiosondedecode as decode
import numpy as np
import matplotlib.pyplot as plt

raw = " TTAA 75001 72501 99016 23414 00000 00158 23020 08503 92836 19831 05506 85562 16657 33004 70186 06012 28009 50588 06982 33015 40758 19778 30020 30965 33325 24543 25090 43946 25054 20236 56545 25059 15415 62961 26051 10665 63177 26524 88164 62962 26063 77180 25068 40918 31313 45208 82306 51515 10164 00004 10194 05004 32505".split()
data = decode.process(raw)
surfacepressure = decode.surface(raw[3])

cleandata = [[], []]

for dpoint in range(len(data[0])):
    if data[0][dpoint] != "n":
        cleandata[0].append(data[0][dpoint])

for dpoint in range(len(data[1])):
    if data[1][dpoint] != "n":
        cleandata[1].append(data[1][dpoint])

yaxis = [1001, 1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100]

while len(yaxis) > len(cleandata[0]):
    yaxis.pop(1)

yaxis[0] = surfacepressure



plt.yscale('log')
plt.plot(cleandata[0], yaxis)
plt.plot(cleandata[1], yaxis)
plt.axis([-100, 50, 1000, 100])

plt.show()
