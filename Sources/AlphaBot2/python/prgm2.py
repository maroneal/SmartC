import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import time

TRIG = 22
ECHO = 27
PWM = 50
DR = 16
DL = 19

Ab = AlphaBot2()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

kit.servo[0].actuation_range = 180
kit.servo[1].actuation_range = 180
kit.servo[0].set_pulse_width_range(500,2500)
kit.servo[1].set_pulse_width_range(500,2500)

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
    return((t2-t1)*34000/2)

def stop_servos():
    kit.servo[0].set_pulse_width_range(0,0)
    kit.servo[1].set_pulse_width_range(0,0)
    kit.servo[0].fraction = 0
    kit.servo[1].fraction = 0

kit.servo[0].angle = 90
kit.servo[1].angle = 90
stop_servos()
try:
    while True:
        
        Dist = dist()
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        Ab.setPWMA(PWM)
        Ab.setPWMB(PWM)
        if Dist <= 30 and Dist >= 20:
            PWM = 30
        elif Dist < 20 and Dist - 5 >= 0:
            PWM = int(Dist)-5
            if((DL_status == 1) or (DR_status == 0)):
                Ab.left()
            elif((DL_status == 0) or (DR_status == 1)):
                Ab.right()
            elif((DL_status == 0) or (DR_status == 0)):
                Ab.backward()
        else:
            Ab.forward()
            PWM = 50
        time.sleep(0.02)
        if PWM <= 6:
            Ab.stop()
        
except KeyboardInterrupt:
    stop_servos()
    Ab.stop()
    GPIO.cleanup();
