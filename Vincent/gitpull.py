import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(7,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(17,GPIO.IN)

try:
	while True:
		if GPIO.input(7) == 0:
			os.system("git pull https://github.com/maroneal/SmartC.git")
			time.sleep(0.5)
			print("SmartC repository updated.")
			GPIO.output(4,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(4,GPIO.LOW)
			time.sleep(0.2)
			GPIO.output(4,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(4,GPIO.LOW)

except KeyboardInterrupt:
	GPIO.cleanup()
