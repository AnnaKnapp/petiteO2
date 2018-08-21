import numpy
import scipy
import matplotlib as mpl
import csv
import time
import matplotlib.pyplot as plt
import tkinter

volts = []
times = []

with open('test_w_returnpath0.txt', newline='') as csvfile:
    datareader = csv.reader(csvfile)
    csv.reader
    starttime = time.time()
    for row in datareader:
        times.append(row[0])
        volts.append(row[1])
    endtime = time.time()
    print(endtime - starttime)
plt.plot(time,volts)
plt.show()
        