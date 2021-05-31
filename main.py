from ConnectionUI import *
from ConnectionPixhawk import *
from ManualControl import *
#from Pixycam import *



master = ConnectToPixhawk()

def Control(arm_disarm, roll, pitch, yaw, throttle, flight_mode):
	Arm_Disarm(master, arm_disarm)
	Move(master, roll, pitch, yaw, throttle, 0)
	ChangeFlightMode(master, flight_mode)
	

def Run():
	commands = Receive()
	master.recv_match()
	if(commands != None):
		#print(str(commands))
		
		Control(commands['arm_disarm'],commands['roll'],commands['pitch'],commands['yaw'],commands['throttle'], commands['flight_mode'])
		#PixyLamp(commands['pixyLight']

		send = {
			"arm_disarm":master.motors_armed(), 
		        "flight_mode":master.flightmode, 
     	 	        "pressure":0, 
		        "clamp": False,
			"light": False,
			"throttle":commands['throttle'],
			"roll":commands['roll'],
			"pitch":commands['pitch'],
			"yaw":commands['yaw']
		       }
		send = json.dumps(send)
		send = str(send)
		#print(str(bool(master.motors_armed())))
		#print(send)
		#send = GetPixyTarget()
		

		Send(bytearray(send,"UTF-8"))
			
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

