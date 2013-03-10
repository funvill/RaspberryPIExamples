# Blinkly Script 
# This script will blink a LED ON and OFF again. 
# 
# Created on Feb 2, 2013 by Steven Smethurst
# Version: 1.00 
# 
# Directions 
# Connect a LED between Pin 6 ( Ground) and pin 12 (GPIO18) 
#  

from time import sleep
import RPi.GPIO as GPIO

# print about info 
print "Blinky script, v1.0" 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT )
while 1: 
	GPIO.output(12, GPIO.HIGH ) 
	sleep(1)
	GPIO.output(12, GPIO.LOW ) 
	sleep(1)
	