

#define the gpio pins you are using for communication outside of spi
#pinmode is BCM
STRT = 26 #start pin - output from pi to ADC
PWDN  = 27 #power down - output from pi to ADC
DRDY  = 17 #data ready - input from ADC to pi

spiBus = 0 #this selects which pins will be used for the SPI communication. For more information refer to raspberry pi documentation