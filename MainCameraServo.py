import RPi.GPIO as GPIO
from time import sleep
pinOut = 5

MAXAngle = 160
MINAngle = 20
pitchAngle = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinOut, GPIO.OUT)
pwm=GPIO.PWM(pinOut, 50)
pwm.start(0)

def SetAngle(pin, angle):
	duty = angle / 18 + 2
	GPIO.output(pin, True)
	pwm.ChangeDutyCycle(duty)
	sleep(.1)
	GPIO.output(pin, False)
	pwm.ChangeDutyCycle(0)



def MoveMainCamera(angle):
	global pitchAngle
	if(angle != pitchAngle):
		if(angle >= MAXAngle):
			SetAngle(pinOut, MAXAngle)
		elif(angle <= MINAngle):
			SetAngle(pinOut, MINAngle)
		else:
			SetAngle(pinOut, angle)
	pitchAngle = angle
	return pitchAngle



if __name__ == "__main__":
	try:
		SetAngle(pinOut,180) 
		pwm.stop()
		GPIO.cleanup()
	except Exception as e:
		print(e)
