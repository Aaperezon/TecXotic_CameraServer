from gpiozero import Servo,AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()


class ServoManager:
	def __init__(self, pin_gpio):
		self.servo = Servo(pin_gpio, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
		self.MAX_angle = 90
		self.MIN_angle = -90
		self.angle = self.MIN_angle
	def SetMaxAngle(self,new_max_angle):
		self.MAX_angle = new_max_angle
	def SetMinAngle(self,new_min_angle):
		self.MIN_angle = new_min_angle
	def remap(self,x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	def SetAngle(self,angle):
		angle = self.remap(angle, self.MIN_angle, self.MAX_angle, -1, 1)
		self.servo.value = angle
	def MoveServo(self,direction, speed):
        	if direction == 'u' and self.angle < self.MAX_angle:
                	self.SetAngle(self.angle + speed)
                	self.angle = self.angle + speed
        	elif direction == 'd' and self.angle > self.MIN_angle:
                	self.SetAngle(self.angle - speed)
                	self.angle = self.angle - speed
	def GetAngle(self):
		return self.angle

if __name__ == "__main__":
	pitch_servo = ServoManager(17)
	try:
		while True:
			instruction = 'u'
			pitch_servo.MoveServo(instruction,1)
			print(pitch_servo.GetAngle())
	except Exception as e:
		print(e)
