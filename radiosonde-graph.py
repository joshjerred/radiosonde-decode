import pylab
import radiosondedecode as decode
import numpy as np
import matplotlib.pyplot as plt

raw = " TTAA 76121 72572 99873 23067 13504 00064 ///// ///// 92771 ///// ///// 85522 25070 14511 70192 13669 15004 50590 11136 36009 40758 20788 24515 30965 32989 23538 25092 39987 21548 20241 50384 22554 15423 61780 23040 10671 67379 23516 88140 64580 24043 77999 31313 58208 81133 51515 10164 00051 10194 16007 18504".split()
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
