import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

DR = 16
DL = 19
BUZ = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(BUZ,GPIO.OUT)


try:
    while True:
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
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
            Ab.stop()
            
except KeyboardInterrupt:
    GPIO.cleanup();

