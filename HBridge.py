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
	left_motor = HBridge(13,19,26)
	right_motor = HBridge(16,20,21)
	try:
		while True:
			a = input("Instruction: ")
			if a == "f":
				left_motor.Forward()
				right_motor_Forward()
			elif a == "b":
				left_motor.Backward()
				right_motor.Backward()
			elif a == "l":
				left_motor.Stop()
				right_motor.Forward()
			elif a == "r":
				left_motor.Forward()
				right_motor.Stop()
			else:
				pass
	except Exception as e:
		print(e)
