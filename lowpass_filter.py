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
#volts = numpy.empty(1,dtype = numpy.float32)
#times = numpy.empty(1,dtype = numpy.float32)
graphdata = open(fileName, 'r').read()
lines = graphdata.split('\n')
starttime = time.time()
for line in lines:
    if len(line)>1:
        x,y = line.split(',')
        times.append(float(x))
        volts.append(float(y))

#times = times[18000:25000]
#volts = volts[18000:25000]

timestep =[]
for i in range(len(times)-1):
    timestep.append(times[i+1] - times[i])
avgTstep = numpy.average(timestep)
print(avgTstep)
N = len(volts)
voltsFft = numpy.fft.fft(volts)
freqs = numpy.linspace(0,1/avgTstep,N)


samplingFreq = 1/avgTstep
nyq = 0.5 * samplingFreq
cutoff = 20 / nyq
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
plt.xlabel('frequency (Hz)')
plt.plot(freqs[:N //2], numpy.abs(voltsFft)[:N//2]*1/N, 'r')
plt.plot(freqs[:N //2], numpy.abs(filteredVoltsBandFft)[:N//2]*1/N, 'b')
plt.show()

