
from gpiozero import OutputDevice



class RelayManager():
	def __init__(self, pin):
		self.relay = OutputDevice(pin)
	def Switch(self, state):
		if state == True:
			self.relay.off()
		elif state == False:
			self.relay.on()

if __name__ == "__main__":
<<<<<<< HEAD
	#led1 = RelayManager(2)
	led2 = RelayManager(3) #front and down light
	cam  = RelayManager(4) #purple
	try:
		while True:
			state = bool(input("state: "))
			#led1.Switch(state)
=======
	led1 = RelayManager(2)
	led2 = RelayManager(3)
	cam  = RelayManager(4)
	try:
		while True:
			state = bool(input("state: "))
			led1.Switch(state)
>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4
			led2.Switch(state)
			cam.Switch(state)
	except Exception as e:
		led1.Switch(0)
		#led2.Switch(0)
		pass
