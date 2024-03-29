import HBridge

left_motor = HBridge.HBridge(13,19,26)
right_motor = HBridge.HBridge(16,20,21)
reel = HBridge.HBridge(0,5,6)
def MoveMiniROV(direction):
	if direction == "f":
		right_motor.Forward()
		left_motor.Backward()
	elif direction == "b":
		right_motor.Backward()
		left_motor.Forward()
	elif direction == "l":
		left_motor.Forward()
		right_motor.Forward()
	elif direction == "r":
		left_motor.Backward()
		right_motor.Backward()
	else:
		left_motor.Stop()
		right_motor.Stop()

def MoveReel(direction):
	if direction == "f":
		reel.Forward()
	elif direction == "b":
		reel.Backward()
	else:
		reel.Stop()
