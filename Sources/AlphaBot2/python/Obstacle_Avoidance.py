import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2
Ab = AlphaBot2()

TRIG = 22
ECHO = 27
DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

def Distance():
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
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        if Dist <= 20:
            Ab.setPWMA(20)
            Ab.setPWMB(20)
        if((DL_status == 1) and (DR_status == 0)):
            print("obstacle on the left")
            Ab.right()
            time.sleep(0.002)
            Ab.stop()
        elif((DL_status == 0) and (DR_status == 1)):
                #GPIO.output(BUZ,GPIO.HIGH)
            print("obstacle on the right")
            Ab.left()
            time.sleep(0.002)
            Ab.stop()
        elif((DL_status == 0) and (DR_status == 0)):
            Ab.backward()
            time.sleep(0.002)
            Ab.stop()
        else:
            Ab.forward()
        time.sleep(0.02)
except KeyboardInterrupt:
    GPIO.cleanup();