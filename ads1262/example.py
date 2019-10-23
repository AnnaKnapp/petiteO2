import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
import ads1262_module as adc

fileName = sys.argv[1] + '.txt'

adc.init_GPIO_SPI

adc.restart

adc.write_all_regs

adc.read_all_regs

print("finished")

datafile = open(fileName, 'w')
startime = time()
errorcount=0
while 1:
    GPIO.output(STRT, 1)
    incoming = GPIO.wait_for_edge(DRDY, GPIO.FALLING, timeout=100)
    datain = spi.readbytes(6)
    GPIO.output(STRT, 0)
    if datain[5] != sum(datain[1:5])+0x9B & 255:
        print("ERR - checksum failed")
    combined_data = datain[1] << 24 | datain[2] << 16 | datain[3] << 8 | datain[4]
    if(combined_data & (1<<31)) !=0:
        combined_data = combined_data - (1<<32)
    O2_data = combined_data*(2.5/2**31)
    timeSoFar = str(time() - startime)
    stringToWrite = timeSoFar +','+ str(O2_data) + '\n'
    datafile.write(stringToWrite)


