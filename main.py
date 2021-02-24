from ConnectionUI import *
from ConnectionPixhawk import *
from ManualControl import *
from Pixycam import *



master = ConnectToPixhawk()

def Control(commands):
	Arm_Disarm(master, commands['arm_disarm'])
	Move(master, commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'], 0)
	pass



def Run():
	commands = Receive()
	if(commands != None):
		print(str(commands))
		
		Control(commands)
		
		#send = """{"target_x":0, "target_y":0, "target_width":30, "target_height":100}"""
		send = GetPixyTarget()
		print(send)		

		Send(bytearray(send))
			
		#PixyLamp(command['pixyLight'])

		

















if __name__ == "__main__":
	try:
		print("Running...")
		while True:
			Run()
	except KeyboardInterrupt:
		CloseConnection()
	except Exception as e:
		print(e)

