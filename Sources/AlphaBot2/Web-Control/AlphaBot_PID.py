import RPi.GPIO as GPIO
import time



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

class AlphaBot(object):
    
    def __init__(self,in1=13,in2=12,ena=6,in3=21,in4=20,enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        GPIO.setup(self.IN3,GPIO.OUT)
        GPIO.setup(self.IN4,GPIO.OUT)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self):
        KP = 0.055
        KI = 0.004
        KD = 0.003
        TARGET = 150
        e1_prev_error = 0
        e2_prev_error = 0

        e1_sum_error = 0
        e2_sum_error = 0
        m1_speed = 0
        m2_speed = 0
        global counts
        global Encoder_A
        global Encoder_A_old
        global Encoder_B_old
        global Encoder_B
        global error
        global rcounts
        global rEncoder_A
        global rEncoder_A_old
        global rEncoder_B_old
        global rEncoder_B
        global rerror
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1,GPIO.HIGH)
        GPIO.output(self.IN2,GPIO.LOW)
        GPIO.output(self.IN3,GPIO.HIGH)
        GPIO.output(self.IN4,GPIO.LOW)
        
        e1_error = TARGET - counts
        e2_error = TARGET - rcounts
        print(e1_error)
        print(e2_error)
        m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m2_speed += (e2_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)
        m1_speed = max(min(100, m1_speed), 0)
        m2_speed = max(min(100, m2_speed), 0)
        self.setPWMA(m1_speed)
        self.setPWMB(m2_speed)
        print("e1 {} e2 {}".format(counts, rcounts))
        print("m1 {} m2 {}".format(m1_speed, m2_speed))

        counts = 0
        rcounts = 0
        #time.sleep(0.1)
        
        e1_prev_error = e1_error
        e2_prev_error = e2_error

        e1_sum_error += e1_error
        e2_sum_error += e2_error

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1,GPIO.LOW)
        GPIO.output(self.IN2,GPIO.LOW)
        GPIO.output(self.IN3,GPIO.LOW)
        GPIO.output(self.IN4,GPIO.LOW)

    def backward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1,GPIO.LOW)
        GPIO.output(self.IN2,GPIO.HIGH)
        GPIO.output(self.IN3,GPIO.LOW)
        GPIO.output(self.IN4,GPIO.HIGH)

    def left(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1,GPIO.HIGH)
        GPIO.output(self.IN2,GPIO.LOW)
        GPIO.output(self.IN3,GPIO.HIGH)
        GPIO.output(self.IN4,GPIO.LOW)

    def right(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1,GPIO.HIGH)
        GPIO.output(self.IN2,GPIO.LOW)
        GPIO.output(self.IN3,GPIO.HIGH)
        GPIO.output(self.IN4,GPIO.LOW)
        
    def setPWMA(self,value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def setPWMB(self,value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)  
        
    def setMotor(self, left, right):
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.IN3,GPIO.HIGH)
            GPIO.output(self.IN4,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.IN3,GPIO.LOW)
            GPIO.output(self.IN4,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

if __name__=='__main__':

    Ab = AlphaBot()
    Ab.forward()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
