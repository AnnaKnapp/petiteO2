import py_ads1262 as ads1262

print(ads1262.POWER)

# ads1262.init()


# readreg_intf = ads1262.RREG | ads1262.MODE2
# while 1:
# 	ads1262_Reg_Write(INTERFACE, 0x05)
# 	spi.xfer([readreg_intf, 0x00])
# 	incoming_reg_bytes = spi.readbytes(1)
# 	sleep(.001)
# 	print(incoming_reg_bytes)