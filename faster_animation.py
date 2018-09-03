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

fig = plt.gcf()
fig.show()
fig.canvas.draw()

while True:
    graphdata = open(fileName, 'r').read()
    lines = graphdata.split('\n')
    xs=[]
    ys=[]
    for line in lines:
        if len(line) > 1:
            x,y = line.split(',')
            xs.append(x)
            ys.append(y)
    if len(xs) >= 700:    #uncomment these 3 lines to have the graph move and only show 100 pts at a time
        xs = xs[-700:-1]
        ys = ys[-700:-1]
    plt.plot(xs,ys)
    fig.canvas.draw()