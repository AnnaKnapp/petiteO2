import spidev
import RPi.GPIO as GPIO
import pigpio
from time import sleep
from time import time
import sys
import ads1262_module as adc
import os

os.nice(-15)

spi = spidev.SpiDev()

pi = pigpio.pi()
pi.set_mode(adc.DRDY, pigpio.INPUT)
pi.set_pull_up_down(adc.DRDY, pigpio.PUD_UP)


GPIO.setmode(GPIO.BCM)
GPIO.setup(adc.STRT, GPIO.OUT) #start pin at gpio pin 4 - output
#GPIO.setup(adc.DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
GPIO.setup(adc.PWDN, GPIO.OUT) #PWDN pin
spi.open(adc.spiBus,0) # (bus, device)??
spi.mode = 0b01
spi.max_speed_hz = 1400000000/adc.clockDiv

fileName = sys.argv[1] + '.txt'

adc.init_GPIO_SPI()

adc.restart()

adc.write_all_regs()

adc.read_all_regs()

print("finished")



GPIO.output(adc.STRT, 1)
datafile = open(fileName, 'w')
startime = time()
errorcount=0

def newdata(A,B,C):
    datain = spi.readbytes(6)
    if datain[5] != sum(datain[1:5])+0x9B & 255:
        print("ERR - checksum failed")
    combined_data = datain[1] << 24 | datain[2] << 16 | datain[3] << 8 | datain[4]
    if(combined_data & (1<<31)) !=0:
        combined_data = combined_data - (1<<32)
    O2_data = combined_data*(2.5/2**31)
    timeSoFar = str(time() - startime)
    stringToWrite = timeSoFar +','+ str(O2_data) + '\n'
    datafile.write(stringToWrite)

while 1:
    pi.callback(adc.DRDY, pigpio.FALLING_EDGE, takedata)




