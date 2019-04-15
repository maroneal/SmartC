import RPi.GPIO as GPIO
import time

TRIG = 22
ECHO = 27

Ab = AlphaBot2()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)

def dist():
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
		pass
	t1 = time.time()
	while GPIO.input(ECHO):
		pass
	t2 = time.time()
	return (t2-t1)*34000/2
	
try:
	while True:
		Dist = Distance()
		print("Distance = %0.2f cm"%Dist)
		if Dist <= 30:
			PWM = 30
			Ab.setPWMA(PWM)
			Ab.setPWMB(PWM)
		elif Dist <= 20 and Dist >= 5:
			Ab.setPWMA(PWM-(1/Dist*100)
			Ab.setPWMB(PWM-(1/Dist*100)
		else:
			Ab.forward()
		time.sleep(0.02)

except KeyboardInterrupt:
	GPIO.cleanup();