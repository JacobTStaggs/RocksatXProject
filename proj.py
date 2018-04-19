#!/usr/bin/python
from __future__ import division
import time
import os


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import the PCA9685 module for the Servos to Operate Correctly.
import Adafruit_PCA9685

# Import the Paths Library to check if Files Exist.
from pathlib import Path

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
xaxis = Adafruit_PCA9685.PCA9685(0x70)
yaxis = Adafruit_PCA9685.PCA9685(0x40)

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Change to Directory for future Astrometry Program Call
os.chdir('/usr/local/astrometry/bin')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VARIOUS GLOBAL VARIABLES
# Creates an Initial incremental File System as the tests are run.
fileNumber = 0
#Creates an Initial incremental Degree System as the tests are run.
degree_var = 0
#Creates an Initial incremental Pulse System as the tests are run.
pulse_var = 0


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Custom and configurated Min and Max Values for THESE Servos the Rocket Uses.
# PowerHD 1810MG <-- Servos Used --> 145 Degree Servos
servo_min = 175  # Min pulse length out of 4096
servo_max = 570  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    xaxis.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
xaxis.set_pwm_freq(60)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This is where the OVERALL TIMING, WHILE, and LOOP BEGINS!!!
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set/Begin Timer
main_timer_end = time.time() + 60 *2.5
# While Timer < 2.5 Minutes, Run everything of the following.
while time.time() < main_timer_end:


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    my_file = Path("/usr/local/astrometry/examples/test%s.jpg" % fileNumber)

    # While Loop that Increments the File Name such that no File is overwritten.
    while my_file.is_file():
        fileNumber = fileNumber+1
        my_file = Path("/usr/local/astrometry/examples/test%s.jpg" % fileNumber)

    # my_file is the newest File Path and Name


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #os.system('sudo fswebcam -r 1280x1024 -S 3 --jpeg 50 --save /usr/local/astrometry/examples/apod1111.jpg')
    #os.system('sudo ./solve-field --scale-low 1  --scale-high 45 /usr/local/astrometry/examples/plz.jpg')

    os.system('sudo fswebcam -r 1280x1024 -S 3 --jpeg 50 --save %s' % my_file)

    # FORMULA FOR SERVOS PULSES FROM degrees
    #     Pulse_Value = [(395/145)*degrees]+175
    #     Range: 0 degrees to 145 degrees

    # Increment degree_var AFTER photo_taken BY 20 degrees
    degree_var = degree_var + 20

    # Calculate the Pulse_Var based upon the Formula and degree_var
    if(degree_var<145):
        pulse_var = int(round(((395/145)*degree_var)+175))
    else:
        degree_var = 10
        pulse_var = int(round(((395/145)*degree_var)+175))

    #Move Servos!!
    xaxis.set_pwm(0,0,pulse_var)
    yaxis.set_pwm(0,0,pulse_var)

    #Solve-Field!!!!
    os.system('sudo ./solve-field --cpulimit 30 --scale-low 1 --scale-high 45 %s' % my_file)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The Following is for testing photos pre-launch!! Not for Launch Use!!
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Sets Photo Loop for one time, later to be adapted for time.
    #PhotoTime = True

    # Photo Loop
    #print('Moving servo on channel 0, press Ctrl-C to quit...')
    #while PhotoTime==True:
        # Sets servo to 0 degrees and takes picture1
        #time.sleep(10)  #THIS SHOULD BE REMOVED FOR LAUNCH!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #os.system('sudo fswebcam -r 1280x1024 -S 3 --jpeg 50 --save %s' % my_file)
        # Sets servo to 20 degrees and takes picture2
        #xaxis.set_pwm(0, 0, 230)
        #time.sleep(10)  #THIS SHOULD BE REMOVED FOR LAUNCH!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #os.system('sudo fswebcam -r 1280x1024 -S 3 --jpeg 50 --save /home/pi/Desktop/test2.jpg')
        # /usr/local/astrometry/examples/test2.jpg    Save Location Astrometry
        #xaxis.set_pwm(0, 0, 175)
        #PhotoTime=False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#os.system('sudo poweroff')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
