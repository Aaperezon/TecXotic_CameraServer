import PID
import agentTest
#import Agent1
kP = 0
kI = 0
kD = 0
pid = PID.PID(kP, kI, kD)




def Setup(kP_input, kI_input, kD_input, target):
	global kP, kI, kD
	pid.SetPoint = target
	pid.setKp(kP_input)
	pid.setKi(kI_input)
	pid.setKd(kD_input)



def Run(activate, cap):
	if activate == True:
		test = agentTest.Run(cap)
		if test != None:
			pid.update(test) #parameter is the moving value from the detection
			#print(f"given value to the orientation {pid.output}")
