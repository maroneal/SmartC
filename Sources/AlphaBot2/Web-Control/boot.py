import RPi.GPIO as GPIO
import os
import time
from neopixel import *
from PCA9685 import PCA9685

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

pwm = PCA9685(0x40)
CTR = 7
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR,GPIO.IN,GPIO.PUD_UP)

while True:
        if GPIO.input(CTR) == 0:
            pwm.write(0,0xFF)
            strip.begin()
            strip.setPixelColor(0, Color(0, 255, 0))
            strip.setPixelColor(1, Color(0, 0, 0))
            strip.setPixelColor(2, Color(0, 0, 0))
            strip.setPixelColor(3, Color(0, 0, 0))
            strip.show()
            time.sleep(0.1)
            print("System shutting down...")
            os.system("sudo shutdown -h now")
            #os.chdir("/home/pi/AlphaBot2/python")
            #time.sleep(0.01)
            #os.system("sudo python3 prgm.py")
            
