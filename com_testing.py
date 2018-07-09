
import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time

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
GPIO.setup(DRDY, GPIO.IN) #DRDY pin
GPIO.setup(PWDN, GPIO.OUT) #PWDN pin



#initialize spi
spi = spidev.SpiDev()
spi.open(0,0) # (bus, device)??
spi.mode = 0b01

def ads1262_Reg_Write(reg_adress, data):
	#I beleive this library automatically brings CS low
	#if this doesnt work try spi.xfer2() to keep CS low
	wreg_address = WREG | reg_adress
	spi.xfer(wreg_address)
	spi.xfer(0x00) #number to write to (this is 0 because we write to)
	spi.xfer(data)


def ads1262_Reset():
	GPIO.output(PWDN, 1)
	sleep(.1)
	GPIO.output(PWDN, 0)
	sleep(.1)
	GPIO.output(PWDN, 1)
	sleep(.1)


def ads1262_Hard_Stop():
	GPIO.output(START, 0)
	sleep(.1)


def ads1262_Enable_Start():
	GPIO.output(START, 1)
	sleep(.02)

def ads1262_init():
	ads1262_Reset()
	sleep(.1)
	ads1262_Hard_Stop()
	sleep(.05)
	#add another 300ms delay if this has problems
	ads1262_Reg_Write(POWER, 0x11) 		#Set sampling rate to 125 SPS
	sleep(.01)
	ads1262_Reg_Write(INTERFACE, 0x05)	#Lead-off comp off, test signal disabled
	sleep(.01)
	ads1262_Reg_Write(MODE0, 0x00)		#Lead-off defaults
	sleep(.01)
	ads1262_Reg_Write(MODE1, 0x80)	#Ch 1 enabled, gain 6, connected to electrode in
	sleep(.01)
	ads1262_Reg_Write(MODE2, 0x06)	#Ch 1 enabled, gain 6, connected to electrode in
	sleep(.01)
	ads1262_Reg_Write(INPMUX, 0x01)	#Ch 1 enabled, gain 6, connected to electrode in
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
	ads1262_Enable_Start()


ads1262_init()

while 1:
	timestart = time()
	if GPIO.input(DRDY) == 0:
		timend = time()
		print 1/(timend-timestart)
		bytesin = spi.readbytes(12)