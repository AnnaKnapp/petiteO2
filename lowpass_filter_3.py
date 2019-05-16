import numpy
import scipy
from scipy import signal
import matplotlib as mpl
import csv
import time
import matplotlib.pyplot as plt
import _tkinter
import sys
fileName = sys.argv[1]


volts = []
times = []
tempC = []
#volts = numpy.empty(1,dtype = numpy.float32)
#times = numpy.empty(1,dtype = numpy.float32)
graphdata = open(fileName, 'r').read()
lines = graphdata.split('\n')
starttime = time.time()
for line in lines:
    if len(line)>1:
        x,y, z = line.split(',')
        times.append(float(x))
        volts.append(float(y))
        tempC.append(float(z))        

#times = times[18000:25000]
#volts = volts[18000:25000]

timestep =[]
for i in range(len(times)-1):
    timestep.append(times[i+1] - times[i])
avgTstep = numpy.average(timestep)
N = len(volts)
voltsFft = numpy.fft.fft(volts)
freqs = numpy.linspace(0,1/avgTstep,N)


samplingFreq = 1/avgTstep
print(samplingFreq)
nyq = 0.5 * samplingFreq
cutoff = 15 / nyq
b, a = signal.butter(6, cutoff, 'low')

filteredVoltsBand = signal.lfilter(b,a,volts)

filteredVoltsBandFft = numpy.fft.fft(filteredVoltsBand)


plt.figure(1)
plt.subplot(211)
plt.ylabel('volts')
plt.xlabel('seconds')
plt.plot(times,volts, 'r')
plt.plot(times,filteredVoltsBand, 'b')

plt.subplot(212)
plt.ylabel('Temp in degrees C')
plt.xlabel('seconds')
plt.plot(times, tempC, 'r')
plt.show()

