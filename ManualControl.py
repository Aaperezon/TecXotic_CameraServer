armOn = False
armOff = False




def Move(master, roll, pitch, yaw, thrust, buttons):
	master.mav.manual_control_send(master.target_system,
                pitch,   # -1000 to 1000
                roll,    # -1000 to 1000
                thrust,  # 0 to 1000  ==  500 means neutral throttle
                yaw,     # -1000 to 1000
                buttons)



def Arm_Disarm(master, stateBtn):
	global armOn, armOff
	if(armOn):
		master.arducopter_arm()	
	else:
		master.arducopter_disarm()	
	
	if(stateBtn == True):
		if(not armOff):
			armOn = not armOn
			armOff = True
	else:
		armOff = False


