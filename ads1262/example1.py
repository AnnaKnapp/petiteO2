import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
import ads1262_module as adc
import os

os.nice(-15)

spi = spidev.SpiDev()


GPIO.setmode(GPIO.BCM)
GPIO.setup(adc.STRT, GPIO.OUT) #start pin at gpio pin 4 - output
GPIO.setup(adc.DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
GPIO.setup(adc.PWDN, GPIO.OUT) #PWDN pin
GPIO.setup(13, GPIO.OUT)
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
while 1:
    incoming = GPIO.wait_for_edge(adc.DRDY, GPIO.FALLING, timeout=100)
        if incoming is None:
            print(timeout)
        else:
            datain = spi.readbytes(6)
            GPIO.output(13, 1)
            if datain[5] != sum(datain[1:5])+0x9B & 255:
                print("ERR - checksum failed")
            combined_data = datain[1] << 24 | datain[2] << 16 | datain[3] << 8 | datain[4]
            if(combined_data & (1<<31)) !=0:
                combined_data = combined_data - (1<<32)
            O2_data = combined_data*(2.5/2**31)
            timeSoFar = str(time() - startime)
            stringToWrite = timeSoFar +','+ str(O2_data) + '\n'
            datafile.write(stringToWrite)
            GPIO.output(13, 0)
    


