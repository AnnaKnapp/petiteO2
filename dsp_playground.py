import numpy
import scipy
from scipy import signal
import matplotlib as mpl
import csv
import time
import matplotlib.pyplot as plt
import _tkinter

volts = []
times = []
#volts = numpy.empty(1,dtype = numpy.float32)
#times = numpy.empty(1,dtype = numpy.float32)

graphdata = open('test_w_returnpath0.txt', 'r').read()
lines = graphdata.split('\n')
starttime = time.time()
for line in lines:
    if len(line)>1:
        x,y = line.split(',')
        times.append(float(x))
        volts.append(float(y))

timestep = []
for i in range(len(times)-1):
    timestep.append(times[i+1] - times[i])
avgTstep = numpy.average(timestep)
print(avgTstep)
N = len(volts)
voltsFft = numpy.fft.fft(volts)
freqs = numpy.linspace(0,1/avgTstep,N)

samplingFreq = 1/avgTstep
removedFreq60 = 59.9
normFreq60 = removedFreq60/(samplingFreq/2)
b60, a60 = signal.iirnotch(normFreq60, 30)

filteredVolts60 = signal.lfilter(b60,a60,volts)



removedFreq120 = 120
normFreq120 = removedFreq120/(samplingFreq/2)
b120, a120 = signal.iirnotch(normFreq120, 30)

filteredVolts120 = signal.lfilter(b120,a120,filteredVolts60)



F60voltsFft = numpy.fft.fft(filteredVolts60)
F120voltsFft = numpy.fft.fft(filteredVolts120)


plt.figure(1)
plt.subplot(211)
plt.plot(times,volts, 'r')
plt.plot(times,filteredVolts60, 'c')
plt.plot(times,filteredVolts120, 'k')


plt.subplot(212)
plt.plot(freqs[:N //2], numpy.abs(voltsFft)[:N//2]*1/N, 'r')
plt.plot(freqs[:N //2], numpy.abs(F60voltsFft)[:N//2]*1/N, 'c')
plt.plot(freqs[:N //2], numpy.abs(F120voltsFft)[:N//2]*1/N, 'k')
plt.show()