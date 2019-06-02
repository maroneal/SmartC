#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from bottle import get,post,run,route,request,template,static_file
from AlphaBot_PID import AlphaBot
from PCA9685 import PCA9685
import threading, time
import os
from neopixel import *
from picamera import PiCamera

Ab = AlphaBot()

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)
BUZ = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZ,GPIO.OUT)

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

#Set the Horizontal servo parameters
HPulse = 1500  #Sets the initial Pulse
HStep = 0      #Sets the initial step length
pwm.setServoPulse(0,HPulse)

#Set the vertical servo parameters
VPulse = 1500  #Sets the initial Pulse
VStep = 0      #Sets the initial step length
pwm.setServoPulse(1,VPulse)

strip.begin()
strip.setPixelColor(0, Color(255, 0, 0))
strip.setPixelColor(1, Color(255, 0, 0))
strip.setPixelColor(2, Color(255, 0, 0))
strip.setPixelColor(3, Color(255, 0, 0))
strip.show()

@get("/")
def index():
    return template("index")
    
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')
    
@post("/cmd")
def cmd():
    global HStep,VStep
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    print(code)
    if(speed != None):
        Ab.setPWMA(float(speed))
        Ab.setPWMB(float(speed))
        print(speed)
    if code == "stop":
        HStep = 0
        VStep = 0
        Ab.stop()
        strip.begin()
        strip.setPixelColor(0, Color(0, 255, 0))
        strip.setPixelColor(1, Color(0, 255, 0))
        strip.setPixelColor(2, Color(0, 255, 0))
        strip.setPixelColor(3, Color(0, 255, 0))
        strip.show()
    elif code == "forward":
        Ab.forward()
        strip.begin()
        strip.setPixelColor(0, Color(0, 0, 255))
        strip.setPixelColor(1, Color(0, 0, 255))
        strip.setPixelColor(2, Color(0, 0, 255))
        strip.setPixelColor(3, Color(0, 0, 255))
        strip.show()
    elif code == "play":
        pwm.write(0x00,0x00)
    elif code == "screen":
        strip.begin()
        strip.setPixelColor(0, Color(255, 255, 255))
        strip.setPixelColor(1, Color(255, 255, 255))
        strip.setPixelColor(2, Color(255, 255, 255))
        strip.setPixelColor(3, Color(255, 255, 255))
        strip.show()
        time.sleep(0.5)
        strip.begin()
        strip.setPixelColor(0, Color(0, 0, 0))
        strip.setPixelColor(1, Color(0, 0, 0))
        strip.setPixelColor(2, Color(0, 0, 0))
        strip.setPixelColor(3, Color(0, 0, 0))
        strip.show()
        time.sleep(0.5)
        strip.begin()
        strip.setPixelColor(0, Color(255, 255, 255))
        strip.setPixelColor(1, Color(255, 255, 255))
        strip.setPixelColor(2, Color(255, 255, 255))
        strip.setPixelColor(3, Color(255, 255, 255))
        strip.show()
        os.system("wget http://192.168.0.54:8080/?action=snapshot")
        time.sleep(0.5)
    elif code == "exit":
        pwm.write(0,0xFF)
    elif code == "backward":
        strip.begin()
        strip.setPixelColor(3, Color(125, 255, 0))
        strip.setPixelColor(0, Color(125, 255, 0))
        strip.setPixelColor(2, Color(0, 0, 0))
        strip.setPixelColor(1, Color(0, 0, 0))
        strip.show()
        Ab.backward()
    elif code == "turnleft":
        Ab.left()
        strip.begin()
        strip.setPixelColor(0, Color(0, 0, 255))
        strip.setPixelColor(1, Color(0, 0, 255))
        strip.setPixelColor(2, Color(0, 0, 255))
        strip.setPixelColor(3, Color(0, 0, 255))
        strip.show()
    elif code == "turnright":
        Ab.right()
        strip.begin()
        strip.setPixelColor(0, Color(0, 0, 255))
        strip.setPixelColor(1, Color(0, 0, 255))
        strip.setPixelColor(2, Color(0, 0, 255))
        strip.setPixelColor(3, Color(0, 0, 255))
        strip.show()
    elif code == "up":
        VStep = -10
    elif code == "down":
        VStep = 10
    elif code == "left":
        HStep = 10
    elif code == "right":
        HStep = -10
    return "OK"
    
def timerfunc():
    global HPulse,VPulse,HStep,VStep,pwm
    
    if(HStep != 0):
        HPulse += HStep
        if(HPulse >= 2500): 
            HPulse = 2500
        if(HPulse <= 500):
            HPulse = 500
        #set channel 2, the Horizontal servo
        pwm.setServoPulse(0,HPulse)    
        
    if(VStep != 0):
        VPulse += VStep
        if(VPulse >= 2500): 
            VPulse = 2500
        if(VPulse <= 500):
            VPulse = 500
        #set channel 3, the vertical servo
        pwm.setServoPulse(1,VPulse)   
    
    global t        #Notice: use global variable!
    t = threading.Timer(0.02, timerfunc)
    t.start()


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

run(host="192.168.1.112",port="8000")