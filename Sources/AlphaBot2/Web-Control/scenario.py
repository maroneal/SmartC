KP = 0.055
KI = 0.0004
KD = 0.03
TARGET = 15

#KP = 0.02
#KI = 0.000
#KD = 0.00
#TARGET = 500

import time
import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from neopixel import *
from PCA9685 import PCA9685

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# LED strip configuration:
LED_COUNT      = 4      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.WS2811_STRIP_RGB

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,LED_CHANNEL,LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()
strip.show()

Ab = AlphaBot2()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.IN)
GPIO.setup(9,GPIO.IN)
GPIO.setup(10,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(4,GPIO.OUT)

Encoder_A_old = 0
Encoder_B_old = 0
rEncoder_A_old = 0
rEncoder_B_old = 0

rerror = 0
error = 0
cpt = 0
counts = 0
rcounts = 0

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

m1_speed = 0
m2_speed = 0
e1_prev_error = 0
e2_prev_error = 0
e1_sum_error = 0
e2_sum_error = 0
counter = 0

def turn_left():
    while(rcounts <= 400):
            Ab.left()
            time.sleep(0.01)
    Ab.stop()

def turn_right():
    while(counts <= 400):
            Ab.right()
            time.sleep(0.01)
    Ab.stop()

strip.begin()
strip.setPixelColor(0, Color(255, 0, 0))
strip.setPixelColor(1, Color(255, 0, 0))
strip.setPixelColor(2, Color(255, 0, 0))
strip.setPixelColor(3, Color(255, 0, 0))
strip.show()

def bip_and_blink():
    GPIO.output(4,not GPIO.input(4))
    strip.begin()
    strip.setPixelColor(0, Color(0, 255, 0))
    strip.setPixelColor(1, Color(0, 255, 0))
    strip.setPixelColor(2, Color(0, 255, 0))
    strip.setPixelColor(3, Color(0, 255, 0))
    strip.show()
    time.sleep(0.4)
    GPIO.output(4,not GPIO.input(4))
    strip.begin()
    strip.setPixelColor(0, Color(0, 0, 0))
    strip.setPixelColor(1, Color(0, 0, 0))
    strip.setPixelColor(2, Color(0, 0, 0))
    strip.setPixelColor(3, Color(0, 0, 0))
    strip.show()
    time.sleep(0.4)
    GPIO.output(4,not GPIO.input(4))
    strip.begin()
    strip.setPixelColor(0, Color(0, 255, 0))
    strip.setPixelColor(1, Color(0, 255, 0))
    strip.setPixelColor(2, Color(0, 255, 0))
    strip.setPixelColor(3, Color(0, 255, 0))
    strip.show()
    time.sleep(0.4)
    GPIO.output(4,not GPIO.input(4))
    strip.begin()
    strip.setPixelColor(0, Color(0, 0, 0))
    strip.setPixelColor(1, Color(0, 0, 0))
    strip.setPixelColor(2, Color(0, 0, 0))
    strip.setPixelColor(3, Color(0, 0, 0))
    strip.show()
    GPIO.output(4, GPIO.LOW)
    
pwm.setServoPulse(0,1500)
pwm.setServoPulse(1,1550)

try:
    while True:
	pwm.write(0x00,0x00)
        time.sleep(1)
        
        while(counter <= 3500):
            counter += counts
            Ab.forward()
            e1_error = TARGET - counts
            e2_error = TARGET - rcounts
            m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
            m2_speed += (e2_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)
            m1_speed = max(min(100, m1_speed), 0)
            m2_speed = max(min(100, m2_speed), 0)
            Ab.setPWMA(m1_speed)
            Ab.setPWMB(m2_speed)
            #print("e1 {} e2 {}".format(counts, rcounts))
            counts = 0
            rcounts = 0
            time.sleep(0.01)
            e1_prev_error = e1_error
            e2_prev_error = e2_error
            e1_sum_error += e1_error
            e2_sum_error += e2_error
            
        Ab.stop()
        m1_speed = 10
        m2_speed = 10
        Ab.setPWMA(m1_speed)
        Ab.setPWMB(m2_speed)
        time.sleep(1)
        counts = 0
        rcounts = 0
        
        for i in range(1500,2500,5):  #left
            pwm.setServoPulse(0,i)
            time.sleep(0.002)
        
        for i in range(1500,1200,-5):  #up
            pwm.setServoPulse(1,i)
            time.sleep(0.002)
        
        time.sleep(2)
        
        for i in range(1200,1500,5):  #down
            pwm.setServoPulse(1,i)
            time.sleep(0.002)
        
        for i in range(2500,500,-5):  #right
            pwm.setServoPulse(0,i)
            time.sleep(0.002)
                        
        time.sleep(2)
        turn_right()
        
        for i in range(500,1500,5):  #left
            pwm.setServoPulse(0,i)
            time.sleep(0.002)
        
        time.sleep(1)
        counts = 0
	rcounts = 0
	counter = 0
        while(counter <= 4000):
            counter += counts
            Ab.forward()
            e1_error = TARGET - counts
            e2_error = TARGET - rcounts
            m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
            m2_speed += (e2_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)
            m1_speed = max(min(100, m1_speed), 0)
            m2_speed = max(min(100, m2_speed), 0)
            Ab.setPWMA(m1_speed)
            Ab.setPWMB(m2_speed)
            #print("e1 {} e2 {}".format(counts, rcounts))
            counts = 0
            rcounts = 0
            time.sleep(0.01)
            e1_prev_error = e1_error
            e2_prev_error = e2_error
            e1_sum_error += e1_error
            e2_sum_error += e2_error
            
        Ab.stop()
	time.sleep(1)
        bip_and_blink()
        pwm.write(0,0xFF)
	counter = 0
        m1_speed = 10
        m2_speed = 10
        Ab.setPWMA(m1_speed)
        Ab.setPWMB(m2_speed)
        time.sleep(1)        
        
        #time.sleep(0.01)     
        
except KeyboardInterrupt:
    GPIO.cleanup();
