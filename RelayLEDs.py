from gpiozero import OutputDevice



class RelayManager():
	def __init__(self, pin):
		self.relay = OutputDevice(pin)
	def Switch(self, state):
		if state == True:
			self.relay.on()
		elif state == False:
			self.relay.off()

if __name__ == "__main__":
	led1 = RelayManager(14)
	#led2 = RelayManager(24)
	try:
		while True:
			state = bool(input("state: "))
			led1.Switch(state)
			#led2.Switch(state)
	except Exception as e:
		led1.Switch(0)
		#led2.Switch(0)
		pass
