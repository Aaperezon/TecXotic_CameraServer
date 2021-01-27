from ConnectionUI import *
from ConnectionPixhawk import *
from ManualControl import *

#from pixycam import *


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
		Send(b"Hola esta es una prueba")
			
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

