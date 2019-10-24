import numpy as np

#define the constants
kB = np.float64(1.38e-23) #Boltzman Constant
e0 = np.float64(1.602e-19) #Elementary charge

#define my parameters
tempK1 = np.float64(873.15)
tempK2 = np.float64(874.15)
c1 = np.float64(210000)
c2 = np.float64(210001)
c3 = np.float64(210002)

dV1 = (kB*tempK1)/(4*e0) * (np.log(c1/c2))
dV2 = (kB*tempK2)/(4*e0) * (np.log(c1/c2))
dV3 = (kB*tempK2)/(4*e0) * (np.log(c1/c3))
dV4 = np.float64(-.0045)
tK = ((dV4/np.log(20/25))*4*e0)/kB

print(tK)
print("change in voltage of 1ppm O2 at 600C ")
print(dV1)
print("change in voltage of 1ppm O2 at 601C ")
print(dV2)
print("change in voltage of 2ppm O2 at 600C ")
print(dV3)