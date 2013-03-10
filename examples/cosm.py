# cosm 
# This script will read a digital pin state and send the change of state 
# to https://cosm.com/feeds/102208 
#
# This script is based on this tutorial from Adafruite 
# http://learn.adafruit.com/send-raspberry-pi-data-to-cosm/overview
# 
# Created on Feb 2, 2013 by Steven Smethurst
# Version: 1.00 
# 
# Directions 
# Install EEML - markup language COSM accepts
#	wget -O geekman-python-eeml.tar.gz https://github.com/geekman/python-eeml/tarball/master
# Connect a LED between Pin 6 ( Ground) and pin 12 (GPIO18) 
# Connect a swtich between Pin 6 (ground) and pin 11 (GPIO17) 
#  

#!/usr/bin/env python
from time import sleep
import os
import RPi.GPIO as GPIO
import eeml

# print about info 
print "Cosm, v1.0" 

# CONSTANTS 
PIN_LED       	= 12
PIN_SWITCH		= 11 

# CONFIGURATION 
# COSM variables. The API_KEY and FEED are specific to your COSM account and must be changed 
API_KEY 	= 'XXXXXXXXXX'
FEED 		= 1234567890
API_URL 	= '/v2/feeds/{feednum}.xml' .format(feednum = FEED)



# SETUP 
# set up the GPIO pins. 
GPIO.setmode(GPIO.BOARD)
# Set up the led pin as an output pin 
GPIO.setup(PIN_LED, GPIO.OUT )
# Set the switch pin to an imput pin 
GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set up a variable to hold the last state of the switch pin
last_switch_date = -1 


# Send to cosm
def SendCosm( id, value ) :
	# Send the change of state to https://cosm.com
	# open up your cosm feed
   	pac = eeml.Pachube(API_URL, API_KEY)
   	
   	#send the switch data 
   	pac.update( [eeml.Data(id, value)] )
    
    # send data to cosm
   	print "sending data to cosm" 
   	pac.put()
   	
   	# hang out and do nothing for 10 seconds, avoid flooding cosm
   	sleep(3)	


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
		
		# Send the value to cosm 
		SendCosm( 0, current_switch_state ) 
		
	# Be nice to the system and sleep between checks 
	sleep( 0.5 ) 