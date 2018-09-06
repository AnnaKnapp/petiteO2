import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys

fileName = sys.argv[1] + '.txt'

#define the gpio pins I will be using for communication outside of spi
START = 4
DRDY  = 17
PWDN  = 27

#define commands (calibration commands are not included at this time)

RREG    = 0x20		#Read n nnnn registers starting at address r rrrr
                                #first byte 001r rrrr (2xh)(2) - second byte 000n nnnn(2)
WREG    = 0x40		#Write n nnnn registers starting at address r rrrr
                                #first byte 010r rrrr (2xh)(2) - second byte 000n nnnn(2)
START	= 0x08		#Start/restart (synchronize) conversions
STOP	= 0x0A		#Stop conversion
RDATAC  = 0x10		#Enable Read Data Continuous mode. 
#This mode is the default mode at power-up.
SDATAC	= 0x11		#Stop Read Data Continuously mode
RDATA	= 0x12		#Read data by command; supports multiple read back.



#define ALL of the register addresses
POWER		= 0x01
INTERFACE	= 0x02
MODE0		= 0x03
MODE1		= 0x04
MODE2		= 0x05
INPMUX		= 0x06
OFCAL0		= 0x07
OFCAL1		= 0x08
OFCAL2		= 0x09
FSCAL0		= 0x0A
FSCAL1		= 0x0B
FSCAL2		= 0x0C
IDACMUX		= 0x0D
IDACMAG		= 0x0E
REFMUX		= 0x0F
TDACP		= 0x10
TDACN		= 0x11
GPIOCON		= 0x12
GPIODIR		= 0x13
GPIODAT		= 0x14
ADC2CFG		= 0x15
ADC2MUX		= 0x16
ADC2OFC0	= 0x17
ADC2OFC1	= 0x18
ADC2FSC0	= 0x19
ADC2FSC1	= 0x1A


GPIO.setmode(GPIO.BCM)


GPIO.setup(START, GPIO.OUT) #start pin at gpio pin 4 - output
GPIO.setup(DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
GPIO.setup(PWDN, GPIO.OUT) #PWDN pin
 


#initialize spi
spi = spidev.SpiDev()
spi.open(0,0) # (bus, device)??
spi.mode = 0b01
spi.max_speed_hz = 61000

def ads1262_Reg_Read(reg_address):
    rreg_address = RREG | reg_address
    spi.xfer([rreg_address, 0x00])
    register_byte = spi.readbytes(1)
    print(register_byte)



def ads1262_Reg_Write(reg_address, data):
	#I beleive this library automatically brings CS low
	#if this doesnt work try spi.xfer2() to keep CS low
	wreg_address = WREG | reg_address
	spi.xfer([wreg_address, 0x00, data])
	sleep(.002)



def ads1262_Read_Data():
    spi.xfer2([RDATA])
    adc_data_out = spi.readbytes(6)
    print(adc_data_out)


GPIO.output(PWDN, 0) #turn it off
sleep(.5) #let it have a nap
GPIO.output(PWDN, 1) #turn it on
GPIO.output(START, 0) #Set start low so conversions do not run and DRDY does not pulse
sleep(2)


ads1262_Reg_Write(POWER, 0x13) 		#turn on Aincom level shift for isolated sensors. to turn off change to 0x11
sleep(.01)
ads1262_Reg_Write(INTERFACE, 0x05)	#Lead-off comp off, test signal disabled
sleep(.01)
ads1262_Reg_Write(MODE0, 0x00)		#Lead-off defaults
sleep(.01)
ads1262_Reg_Write(MODE1, 0x03<<5)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)
ads1262_Reg_Write(MODE2,0x00 | 0x08)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)
ads1262_Reg_Write(INPMUX, 0xa) #Ain0 is + input and Aincom is - input. to change please see datasheet
sleep(.01)  
ads1262_Reg_Write(OFCAL0, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(OFCAL1, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(OFCAL2, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(FSCAL0, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(FSCAL1, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(FSCAL2, 0x40)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(IDACMUX, 0xBB)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(IDACMAG, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Write(REFMUX, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(TDACP, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(TDACN, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(GPIOCON, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(GPIODIR, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(GPIODAT, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(ADC2CFG, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(ADC2MUX, 0x01)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(ADC2OFC0, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(ADC2OFC1, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(ADC2FSC0, 0x00)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Write(ADC2FSC1, 0x40)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)


ads1262_Reg_Read(POWER) 		#Set sampling rate to 125 SPS
sleep(.01)
ads1262_Reg_Read(INTERFACE)	#Lead-off comp off, test signal disabled
sleep(.01)
ads1262_Reg_Read(MODE0)		#Lead-off defaults
sleep(.01)
ads1262_Reg_Read(MODE1)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)
ads1262_Reg_Read(MODE2)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)
ads1262_Reg_Read(INPMUX)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(OFCAL0)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(OFCAL1)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(OFCAL2)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(FSCAL0)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(FSCAL1)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(FSCAL2)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(IDACMUX)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(IDACMAG)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)  
ads1262_Reg_Read(REFMUX)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(TDACP)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(TDACN)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(GPIOCON)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(GPIODIR)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(GPIODAT)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(ADC2CFG)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(ADC2MUX)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(ADC2OFC0)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(ADC2OFC1)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(ADC2FSC0)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)    
ads1262_Reg_Read(ADC2FSC1)	#Ch 1 enabled, gain 6, connected to electrode in
sleep(.01)
print("finished")

sleep(1) #long nap before starting the conversion (data reading)


GPIO.output(START, 1) #set start high to begin reading conversion data

datafile = open(fileName, 'w')
startime = time()
while 1:
    if GPIO.input(DRDY) == 0:
        datain = spi.readbytes(6)
        if datain[5] != sum(datain[1:5])+0x9B & 255:
            print("nay")
        combined_data = datain[1] << 24 | datain[2] << 16 | datain[3] << 8 | datain[4]
        if(combined_data & (1<<31)) !=0:
            combined_data = combined_data - (1<<32)
        converted_data = combined_data*(2.5/2**31)
        #if converted_data > 4:
            #print("oops")
        timeSoFar = str(time() - startime)
        stringToWrite = timeSoFar +','+ str(converted_data) + '\n'
        #print(stringToWrite)
        datafile.write(stringToWrite)


