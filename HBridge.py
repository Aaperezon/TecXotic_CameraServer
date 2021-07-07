
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class HBridge:
	def __init__(self,in1,in2,ena,speed=100):
		self.in1 = in1
		self.in2 = in2
		self.ena = ena
		GPIO.setup(self.in1, GPIO.OUT)
		GPIO.setup(self.in2, GPIO.OUT)
		GPIO.setup(self.ena, GPIO.OUT)
		GPIO.output(self.in1, GPIO.LOW)
		motor = GPIO.PWM(ena,1000)
		motor.start(0)
		motor.ChangeDutyCycle(speed)
	def Forward(self):
		GPIO.output(self.in1, GPIO.HIGH)
		GPIO.output(self.in2, GPIO.LOW)
	def Backward(self):
		GPIO.output(self.in1, GPIO.LOW)
		GPIO.output(self.in2, GPIO.HIGH)
	def Stop(self):
		GPIO.output(self.in1, GPIO.LOW)
		GPIO.output(self.in2, GPIO.LOW)
	
if __name__ == "__main__":
	motor1 = HBridge(19,13,26)
	try:
		while True:
			motor1.Forward()
	except Exception as e:
		print(e)
