import RPi.GPIO as GPIO
import time
import os

IR = 17
n = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(7,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(IR,GPIO.IN)

def getkey():
	if GPIO.input(IR) == 0:
		count = 0
		while GPIO.input(IR) == 0 and count < 200:  #9ms
			count += 1
			time.sleep(0.00006)
		if(count < 10):
			return;
		count = 0
		while GPIO.input(IR) == 1 and count < 80:  #4.5ms
			count += 1
			time.sleep(0.00006)

		idx = 0
		cnt = 0
		data = [0,0,0,0]
		for i in range(0,32):
			count = 0
			while GPIO.input(IR) == 0 and count < 15:    #0.56ms
				count += 1
				time.sleep(0.00006)
				
			count = 0
			while GPIO.input(IR) == 1 and count < 40:   #0: 0.56mx
				count += 1                               #1: 1.69ms
				time.sleep(0.00006)
				
			if count > 7:
				data[idx] |= 1<<cnt
			if cnt == 7:
				cnt = 0
				idx += 1
			else:
				cnt += 1
#		print data
		if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
			return data[2]
		else:
			print("repeat")
			return "repeat"


try:
	while True:
		key = getkey()
		if(key != None):
			n = 0				 
			if key == 0x1c:
		#if GPIO.input(7) == 0:
			os.system("cd SmartC")
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
		else:
			n += 1
			if n > 20000:
				n = 0


except KeyboardInterrupt:
	GPIO.cleanup()
