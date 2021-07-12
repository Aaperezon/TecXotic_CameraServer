import HBridge

left_motor = HBridge.HBridge(13,19,26)
right_motor = HBridge.HBridge(16,20,21)

def MoveMiniROV(direction):
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
