# DigitalRead 
# This script will read a digital pin state and print it to the screen 
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
print "Digital Read, v1.0" 

# CONSTANTS 
PIN_LED       	= 12
PIN_SWITCH		= 11 

# SETUP 
# set up the GPIO pins. 
GPIO.setmode(GPIO.BOARD)
# Set up the led pin as an output pin 
GPIO.setup(PIN_LED, GPIO.OUT )
# Set the switch pin to an imput pin 
GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set up a variable to hold the last state of the switch pin
last_switch_date = -1 

# MAIN LOOP 
while 1:
	
	# get the current state of the swtich 
	current_switch_state = GPIO.input(11) 
	
	# if the current state of the swtich has changed since the last time we
	# checked the switch. print the change to the screen and set the led 
	if current_switch_state != last_switch_date :
		last_switch_date = current_switch_state  
		
		# the state of the swtich has change. update the screen 
		print "Switch changed to " + str( current_switch_state )  
		
		# change the led to match the state of the switch 
		GPIO.output(12, current_switch_state ) 
		
	# Be nice to the system and sleep between checks 
	sleep( 0.5 ) 