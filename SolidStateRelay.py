import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class SolidStateRelay:
	def __init__(self, channel):
		self.channel = channel
		GPIO.setup(self.channel, GPIO.OUT)

	def Switch(self, state):
		if state == True:
			GPIO.output(self.channel, GPIO.LOW)
		elif state == False:
			GPIO.output(self.channel, GPIO.HIGH)
if __name__ == "__main__":
	s1 = SolidStateRelay(2) #Downward light
	s2 = SolidStateRelay(3) #Purple ight
	s3 = SolidStateRelay(4) #Front light
	
	try:
		while True:
			i = input("instruction: ")
			s1.Switch(bool(i))
			s2.Switch(bool(i))
			s3.Switch(bool(i))
		
				
	except KeyboardInterrupt:
		camera1.EndStream()
