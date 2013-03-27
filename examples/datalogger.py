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
#    wget -O geekman-python-eeml.tar.gz https://github.com/geekman/python-eeml/tarball/master
# Connect a LED between Pin 6 ( Ground) and pin 12 (GPIO18) 
# Connect a swtich between Pin 6 (ground) and pin 11 (GPIO17) 
#  

#!/usr/bin/env python
from time import sleep


import os
import eeml
import pyfirmata

# print about info 
print "Cosm, v1.1" 

# CONFIGURATION 
# COSM variables. The API_KEY and FEED are specific to your COSM account and must be changed 
API_KEY 	= 'XXXXXXXXXXXXXXXXXXXXX'
FEED 		= 102208
API_URL 	= '/v2/feeds/{feednum}.xml' .format(feednum = FEED)



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
   	# sleep(3)	


def SendCosmTwo( values ) :
    # Send the change of state to https://cosm.com
    # open up your cosm feed
    pac = eeml.Pachube(API_URL, API_KEY)
    
    for point in values:
        pac.update( [eeml.Data(point[0], point[1]) ] )
       
    # send data to cosm
    print "sending data to cosm"
    pac.put()       

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])






def main() :  
    
    print "Connecting to the arduino..." 
    # Create a new board, specifying serial port
    board = pyfirmata.Arduino('/dev/ttyACM0')
    
    # start an iterator thread so that serial buffer doesn't overflow
    it = pyfirmata.util.Iterator(board)
    it.start()
    
    print "Setting up the arduino pins" 
    # set up pins
    pin0=board.get_pin('a:0:i')             # A0 Input      (LM35)
    # pin3=board.get_pin('d:3:p')             # D3 PWM Output (LED)
    
    # IMPORTANT! discard first reads until A0 gets something valid
    while pin0.read() is None:
        pass
    
    
    # MAIN LOOP 
    while 1:
    	
        
        
    	# get the current state of the swtich 
        currentValue = pin0.read()
        
        # map the recived value to a value from 0-100
        # mappedValue = minTo + (maxTo - minTo) * ((value - minFrom) / (maxFrom - minFrom));
        mappedValue = 0 + (100 - 0) * ((currentValue - 0.0) / (0.80 - 0.0));
        
        # print out the value for debug. 
        print "Light Raw=[" + str( currentValue ) + "], Scaled=[" + str( mappedValue ) + "]"      
        
        cosmValues = [[ "light", mappedValue ]]
    
    
        # CPU informatiom
        CPU_temp  = getCPUtemperature()
        CPU_usage = getCPUuse()

        cosmValues += [[ "CPU_temp", str( CPU_temp ) ] ]
        cosmValues += [[ "CPU_usage", str( CPU_usage ) ] ]

        # RAM information
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000,1)
        RAM_used  = round(int(RAM_stats[1]) / 1000,1)
        RAM_free  = round(int(RAM_stats[2]) / 1000,1)
        
        cosmValues += [[ "RAM_total", str( RAM_total ) ] ]
        cosmValues += [[ "RAM_used", str( RAM_used ) ] ]
        cosmValues += [[ "RAM_free", str( RAM_free ) ] ]
        
        # Disk information
        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_free  = DISK_stats[1]
        DISK_perc  = DISK_stats[3]
        
        cosmValues += [[ "DISK_total", str( DISK_total ) ] ]
        cosmValues += [[ "DISK_free", str( DISK_free ) ] ]
        cosmValues += [[ "DISK_perc", str( DISK_perc ) ] ]    
        
        print str( cosmValues ) 
        SendCosmTwo( cosmValues ) 
    
        # Send the data to Cosm
        # SendCosm( "light", mappedValue ) 
        
    	# Be nice to the system and sleep between checks 
        sleep( 10 ) 
        
    # All done     
    board.exit()
    
if __name__ == '__main__':
    main()