#!/usr/bin/python3
import RPi.GPIO as GPIO  
import math, sys, os
import subprocess
import socket

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

c=0
last = 1

def count(pin):
    global c 
    c = c + 1

GPIO.add_event_detect(18, GPIO.BOTH)

while True:
    try:
        if GPIO.event_detected(18):
            current = GPIO.input(18)
            if(last != current):
                if(current == 0):
                    GPIO.add_event_detect(23, GPIO.BOTH, callback=count, bouncetime=8)
                else:
                    GPIO.remove_event_detect(23)
                    print (c)
                                 
                    #print ("You dial", number)

                    c= 0                 
                    
                    
                last = GPIO.input(18)
    except KeyboardInterrupt:
        break
