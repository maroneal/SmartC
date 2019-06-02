#KP = 0.055
#KI = 0.004
#KD = 0.003
#TARGET = 150

KP = 0.02
KI = 0.000
KD = 0.00
TARGET = 500

import time
import os
import RPi.GPIO as GPIO
import math
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.IN)
GPIO.setup(9,GPIO.IN)
GPIO.setup(10,GPIO.IN)
GPIO.setup(11,GPIO.IN)

Encoder_A_old = 0
Encoder_B_old = 0
rEncoder_A_old = 0
rEncoder_B_old = 0

rerror = 0
error = 0
cpt = 0
counts = 0
rcounts = 0
m1_speed = 0
m2_speed = 0

def left_encoderscount(channel):
    global counts
    global Encoder_A
    global Encoder_A_old
    global Encoder_B_old
    global Encoder_B
    global error
    
    Encoder_A,Encoder_B = GPIO.input(8),GPIO.input(9)
    
    if ((Encoder_A,Encoder_B_old) == (1,0)) or ((Encoder_A,Encoder_B_old) == (0,1)):
        # this will be clockwise rotation
        counts += 1
      #  print ("Left Encoder count is %s\nAB is %s %s"%(counts, Encoder_A, Encoder_B))

    elif ((Encoder_A,Encoder_B_old) == (1,1)) or ((Encoder_A,Encoder_B_old) == (0,0)):
        # this will be counter-clockwise rotation
        counts -= 1
      #  print ("Left Encoder count is %s\nAB is %s %s"%(counts, Encoder_A, Encoder_B))

    else:
        #this will be an error
        error += 1
        #print ("Error count is %s"%error)

    Encoder_A_old,Encoder_B_old = Encoder_A,Encoder_B

def right_encoderscount(channel):
    global rcounts
    global rEncoder_A
    global rEncoder_A_old
    global rEncoder_B_old
    global rEncoder_B
    global rerror
    
    rEncoder_A,rEncoder_B = GPIO.input(11),GPIO.input(10)
    
    if ((rEncoder_A,rEncoder_B_old) == (1,0)) or ((rEncoder_A,rEncoder_B_old) == (0,1)):
        # this will be counter-clockwise rotation
        rcounts -= 1
        #print ("Right Encoder count is %s\nAB is %s %s"%(rcounts, rEncoder_A, rEncoder_B))

    elif ((rEncoder_A,rEncoder_B_old) == (1,1)) or ((rEncoder_A,rEncoder_B_old) == (0,0)):
        # this will be clockwise rotation
        rcounts += 1
       # print ("Right Encoder count is %s\nAB is %s %s"%(rcounts, rEncoder_A, rEncoder_B))

    else:
        #this will be an error
        rerror += 1
        #print ("Error count is %s"%error)

    rEncoder_A_old,rEncoder_B_old = rEncoder_A,rEncoder_B

GPIO.add_event_detect(8, GPIO.BOTH, callback = left_encoderscount)
GPIO.add_event_detect(9, GPIO.BOTH, callback = left_encoderscount)
GPIO.add_event_detect(11, GPIO.BOTH, callback = right_encoderscount)
GPIO.add_event_detect(10, GPIO.BOTH, callback = right_encoderscount)

e1_prev_error = 0
e2_prev_error = 0

e1_sum_error = 0
e2_sum_error = 0

try:
    while True:
        Ab.forward()

        e1_error = TARGET - counts
        e2_error = TARGET - rcounts
        print(e1_error)
        print(e2_error)
        m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m2_speed += (e2_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)
        m1_speed = max(min(100, m1_speed), 0)
        m2_speed = max(min(100, m2_speed), 0)
        Ab.setPWMA(m1_speed)
        Ab.setPWMB(m2_speed)
        print("e1 {} e2 {}".format(counts, rcounts))
        print("m1 {} m2 {}".format(m1_speed, m2_speed))
        counts = 0
        rcounts = 0
        time.sleep(0.1)
        
        e1_prev_error = e1_error
        e2_prev_error = e2_error

        e1_sum_error += e1_error
        e2_sum_error += e2_error
        
except KeyboardInterrupt:
    GPIO.cleanup();


