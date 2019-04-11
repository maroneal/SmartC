import RPi.GPIO as GPIO
import os
import time

CTR = 7
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR,GPIO.IN,GPIO.PUD_UP)

while True:
        if GPIO.input(CTR) == 0:
            os.chdir("/home/pi/AlphaBot2/python")
	    time.sleep(0.01)
            os.system("sudo python3 prgm.py")
