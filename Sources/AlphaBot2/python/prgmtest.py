import time
import os
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import math
from picamera import PiCamera
from AlphaBot2 import AlphaBot2
import threading
kit = ServoKit(channels=16)
Ab = AlphaBot2()
camera = PiCamera()

BUZ = 4
IR = 17 #Remote controller
DR = 16 
DL = 19 
PWM = 50
n = 0
TRIG = 22
ECHO = 27
key = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IR,GPIO.IN)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(BUZ,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)

def getkey(key):
    k = 0
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
#       print data
        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
            k = data[2]
        if k == 0x18:
            return 2
        elif k == 0x08:
            return 4
        elif k == 0x1c:
            return 5
        elif k == 0x5a:
            return 6
        elif k == 0x52:
            return 8
        elif k == 0x15:
            return 10
        elif k == 0x07:
            return 11
        elif k == 0x09:
            return 12
        elif k == 0x44:
            return 13
        elif k == 0x40:
            return 14
        elif k == 0x47:
            return 15
        elif k == 0x45:
            return 16
        elif k == 0x16:
            return 17
        else:
            print("repeat")
            return "repeat"

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

def stop_servos():
    kit.servo[0].set_pulse_width_range(0,0)
    kit.servo[1].set_pulse_width_range(0,0)
    kit.servo[0].fraction = 0
    kit.servo[1].fraction = 0
    
print('IRremote Test Start ...')
#camera.start_preview()
kit.servo[0].actuation_range = 180
kit.servo[1].actuation_range = 180
kit.servo[0].set_pulse_width_range(500,2500)
kit.servo[1].set_pulse_width_range(500,2500)
kit.servo[0].angle = 90
kit.servo[1].angle = 90
Ab.stop()
try:
    while True:
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        Dist = dist()
        print("Distance = %0.2f cm"%Dist)
        #print(DR_status,DL_status)
        if((DL_status == 1) and (DR_status == 0)):
            GPIO.output(BUZ,GPIO.HIGH)
            print("obstacle on the left")
            Ab.right()
            time.sleep(0.002)
            Ab.stop()
        elif((DL_status == 0) and (DR_status == 1)):
            GPIO.output(BUZ,GPIO.HIGH)
            print("obstacle on the right")
            Ab.left()
            time.sleep(0.002)
            Ab.stop()
        elif((DL_status == 0) and (DR_status == 0)):
            GPIO.output(BUZ,GPIO.HIGH)
            Ab.backward()
            time.sleep(0.002)
            Ab.stop()
            
        GPIO.output(BUZ,GPIO.LOW)
        key = 0
        thd = threading.Thread(target=getkey, args=(key,))
        thd.start()
        if(key != None):
            n = 0
            i = 0
            if key == 2: #2
                if((DL_status == 1) and (DR_status == 1)):
                    Ab.forward()
                    print("forward")
            if key == 4: #4
                Ab.left()
                print("left")
            if key == 5: #5
                Ab.stop()
                print("stop")
            if key == 6: #6
                Ab.right()
                print("right")
            if key == 8: #8
                Ab.backward()       
                print("backward")
            if key == 10: #+
                if(PWM + 10 < 101):
                    PWM = PWM + 10
                    Ab.setPWMA(PWM)
                    Ab.setPWMB(PWM)
                    print(PWM)
            if key == 11: #-
                if(PWM - 10 > -1):
                    PWM = PWM - 10
                    Ab.setPWMA(PWM)
                    Ab.setPWMB(PWM)
                    print(PWM)
            if key == 12: #EQ
                kit.servo[0].angle = 90
                kit.servo[1].angle = 90                     
            if key == 13: #<<
                print("servo left")
                for i in range(0,400,1):
                    if kit.servo[0].angle < 179:
                        kit.servo[0].angle += 0.002*i
                        time.sleep(0.002)
            if key == 14: #>>
                print("servo right")
                for i in range(0,250,1):
                    if kit.servo[0].angle > 1:
                        kit.servo[0].angle -= 0.001*i
                        time.sleep(0.002)
            if key == 15: #CH+
                print("servo up")
                for i in range(0,250,1):
                    if kit.servo[1].angle > 1:
                        kit.servo[1].angle -= 0.001*i
                        time.sleep(0.002)
            if key == 16: #CH-
                print("servo down")
                for i in range(0,400,1):
                    if kit.servo[1].angle < 179:
                        kit.servo[1].angle += 0.002*i
                        time.sleep(0.002)
            if key == 17: #0
                stop_servos()
                os.sys.exit()
                    
        else:
            n += 1
            if n > 20000:
                n = 0
                Ab.stop()
                       
except KeyboardInterrupt:
    camera.stop_preview()
    GPIO.cleanup();


