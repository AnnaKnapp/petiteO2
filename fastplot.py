import pyqtgraph as pg
import numpy as np
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
avgTstep = np.average(timestep)
print(avgTstep)
N = len(volts)
voltsFft = np.fft.fft(volts)
freqs = np.linspace(0,1/avgTstep,N)



samplingFreq = 1/avgTstep
nyq = 0.5 * samplingFreq
low = 14.0 / nyq
high = 14.1 / nyq
b, a = signal.butter(3, [low, high], btype='band')
filteredVoltsBand = signal.filtfilt(b,a,volts)
multiplied = np.multiply(volts,filteredVoltsBand)


cutoff = 0.5 / nyq
c, d = signal.butter(5, cutoff, 'low')

finalout = signal.filtfilt(c,d,multiplied)

lowpassOnly = finalout = signal.filtfilt(c,d,volts)

#filteredVoltsBand = signal.lfilter(b,a,volts)

filteredVoltsBandFft = np.fft.fft(filteredVoltsBand)
multFft = np.fft.fft(multiplied)
finalFFt = np.fft.fft(finalout)

pg.plot(times, volts, pen=, symbol=None)
