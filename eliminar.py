import RPi.GPIO as GPIO          
from time import sleep

in1 = 16
in2 = 20
in3 = 13
in4 = 19

en1 = 21
en2 = 26

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
motor1=GPIO.PWM(en1,1000)
motor2=GPIO.PWM(en2,1000)
motor1.start(0)
motor2.start(0)

def MoveMiniROV(direction):
    if(direction == "f"):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    elif(direction == "b"):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    elif(direction == "l"):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    elif(direction == "r"):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
    else:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

def SetSpeed(speed):
    motor1.ChangeDutyCycle(speed)
    motor2.ChangeDutyCycle(speed)
SetSpeed(100)


if __name__ == "__main__":
    try:
        SetSpeed(50)
        while True:
            entrada = str(input("direccion: "))
            MoveMiniROV(entrada)
    except Exception as e:
        print(e)
