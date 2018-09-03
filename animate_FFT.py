import numpy
import scipy
from scipy import signal
import matplotlib as mpl
import csv
import time
import matplotlib.pyplot as plt
import _tkinter
import matplotlib.animation as animation
from matplotlib import style
import sys

fileName = sys.argv[1] + '.txt'

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)


def animate(i):
    graphdata = open(fileName, 'r').read()
    lines = graphdata.split('\n')
    times=[]
    volts=[]
    timestep =[]
    for i in range(1,600):
    	line = lines[i*-1]
    	if len(line) > 19:
            x,y = line.split(',')
            times.append(x)
            volts.append(y)
    ax1.clear()
    ax1.plot(times,volts)

    for i in range(len(times)-1):
        timestep.append(float(times[i+1]) - float(times[i]))
    avgTstep = numpy.average(timestep)
    print(avgTstep)
    N = len(volts)
    voltsFft = numpy.fft.fft(volts)
    freqs = numpy.linspace(0,1/avgTstep,N)  
    ax2.clear
    ax2.plot(freqs, voltsFft)

ani = animation.FuncAnimation(fig, animate, interval = 1)
plt.show()
