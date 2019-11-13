import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


#define the constants
kB = np.float64(1.38e-23) #Boltzman Constant
e0 = np.float64(1.602e-19) #Elementary charge

#define my parameters
tempK1 = np.float64(873.15)

times = np.linspace(0,30,36000)
#O2_central = 10*np.sin(82*times)+210000
O2_central = 250*signal.sawtooth(2 * np.pi * 13 * times, 0.5)+210000
O2_outside1 = np.float64(210000)
O2_outside2 = np.float64(210001)
volts1 = (kB*tempK1)/(4*e0) * (np.log(O2_central/O2_outside1))
volts2 = (kB*tempK1)/(4*e0) * (np.log(O2_central/O2_outside2))
#volts1 = (kB*tempK1)/(4*e0) * (np.log((1000*times+20000)/O2_outside1))

peaks, h = signal.find_peaks(volts1)

plt.figure(1)
plt.subplot(211)
plt.ylabel('O2 inside')
plt.xlabel('seconds')
plt.plot(times,O2_central, 'r')

plt.subplot(212)
plt.xlabel('time')
plt.plot(times , volts2, 'b')
plt.plot(times , volts1, 'r')
#plt.plot(times[peaks], volts1[peaks], 'o')
plt.show()