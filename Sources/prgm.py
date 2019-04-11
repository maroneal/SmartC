import time
import os
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import math
from picamera import PiCamera
from AlphaBot2 import AlphaBot2
kit = ServoKit(channels=16)
Ab = AlphaBot2()
camera = PiCamera()

BUZ = 4
IR = 17 #Remote controller
DR = 16 
DL = 19 
PWM = 50
n = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IR,GPIO.IN)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(BUZ,GPIO.OUT)

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
#       print data
        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
            return data[2]
        else:
            print("repeat")
            return "repeat"

            
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
        key = getkey()
        if(key != None):
            n = 0
            i = 0
            if key == 0x18: #2
                if((DL_status == 1) and (DR_status == 1)):
                    Ab.forward()
                    print("forward")
            if key == 0x08: #4
                Ab.left()
                print("left")
            if key == 0x1c: #5
                Ab.stop()
                print("stop")
            if key == 0x5a: #6
                Ab.right()
                print("right")
            if key == 0x52: #8
                Ab.backward()       
                print("backward")
            if key == 0x15: #+
                if(PWM + 10 < 101):
                    PWM = PWM + 10
                    Ab.setPWMA(PWM)
                    Ab.setPWMB(PWM)
                    print(PWM)
            if key == 0x07: #-
                if(PWM - 10 > -1):
                    PWM = PWM - 10
                    Ab.setPWMA(PWM)
                    Ab.setPWMB(PWM)
                    print(PWM)
            if key == 0x09: #EQ
                kit.servo[0].angle = 90
                kit.servo[1].angle = 90                     
            if key == 0x44: #<<
                print("servo left")
                for i in range(0,400,1):
                    if kit.servo[0].angle < 179:
                        kit.servo[0].angle += 0.002*i
                        time.sleep(0.002)
            if key == 0x40: #>>
                print("servo right")
                for i in range(0,250,1):
                    if kit.servo[0].angle > 1:
                        kit.servo[0].angle -= 0.001*i
                        time.sleep(0.002)
            if key == 0x47: #CH+
                print("servo up")
                for i in range(0,250,1):
                    if kit.servo[1].angle > 1:
                        kit.servo[1].angle -= 0.001*i
                        time.sleep(0.002)
            if key == 0x45: #CH-
                print("servo down")
                for i in range(0,400,1):
                    if kit.servo[1].angle < 179:
                        kit.servo[1].angle += 0.002*i
                        time.sleep(0.002)
            if key == 0x16: #0
                kit.servo[0].set_pulse_width_range(0,0)
                kit.servo[1].set_pulse_width_range(0,0)
                kit.servo[0].fraction = 0
                kit.servo[1].fraction = 0
                os.sys.exit()
                    
        else:
            n += 1
            if n > 20000:
                n = 0
                Ab.stop()
                       
except KeyboardInterrupt:
    camera.stop_preview()
    GPIO.cleanup();


