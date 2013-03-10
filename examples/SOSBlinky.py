# Blinkly Script 
# This script will blink a LED ON and OFF again in the SOS pattern. 
# Showes how to use the sleep command. 
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
print "SOS Blinky script, v1.0" 

# CONSTANTS 
PIN_LED       = 12
SHORT_TIME    = 0.1
LONG_TIME     = 0.5

# SETUP 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_LED, GPIO.OUT )

def Blink( pin, time ) :
	sleep(time)	
	GPIO.output(pin, GPIO.HIGH ) 
	sleep(time)	
	GPIO.output(pin, GPIO.LOW ) 
	
# MAIN LOOP 
while 1: 
	
	# Three short 
	Blink( PIN_LED, SHORT_TIME ); 
	Blink( PIN_LED, SHORT_TIME ); 
	Blink( PIN_LED, SHORT_TIME ); 
	
	# THREE LONG BLASTS 
	Blink( PIN_LED, LONG_TIME );
	Blink( PIN_LED, LONG_TIME ); 
	Blink( PIN_LED, LONG_TIME ); 
	
