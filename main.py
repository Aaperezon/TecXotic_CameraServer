from ConnectionUI import *
from ConnectionPixhawk import *
from ManualControl import *
from MainCameraServo import *
from ManualControlMiniROV import *
from CameraStream import *
indicator_pixhawk = False
indicator_pitch_camera=0


pixhawk_status = False
pixhawkWarning = False
master = None
camera1 = CameraStream('0')
camera2 = CameraStream('2')
camera1.Run()
camera2.Run()
def Control(arm_disarm, roll, pitch, yaw, throttle, flight_mode, connect_pixhawk):
	global indicator_pixhawk, pixhawkWarning, master
	if(master != None):
		master.recv_match()
		Arm_Disarm(master, arm_disarm)
		Move(master, roll, pitch, yaw, throttle, 0)
		ChangeFlightMode(master, flight_mode)
		indicator_pixhawk = True
		master = ConnectDisconnectPixhawk(connect_pixhawk)

	else:
		indicator_pixhawk = False
		master = ConnectDisconnectPixhawk(connect_pixhawk)
		#LightsManager.KillThread()
		#LightsManager.AssignThread(LightsManager.WarningConnectionPixhawk)


def UtilityControl(pitch_camera,miniROV_direction,cam_port1, cam_port2):
	global indicator_pitch_camera
	#indicator_pitch_camera = MoveMainCamera(pitch_camera)
	#MoveMiniROV(miniROV_direction)
	camera1.SaveCameraPort(int(cam_port1))
	camera2.SaveCameraPort(int(cam_port2))
def Run():
	global pixhawk_status
	commands = Receive()
	if(commands != None):
		#print(str(commands))
		Control(commands['arm_disarm'],commands['roll'],commands['pitch'],commands['yaw'],commands['throttle'], commands['flight_mode'], commands['connect_pixhawk'])
		UtilityControl(commands['pitch_camera'], commands['miniROV_direction'],commands['cam_port1'],commands['cam_port2'])

		send = {
				"connection_pixhawk": indicator_pixhawk,
				"pitch_camera" : indicator_pitch_camera,
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
		#print(commands['connect_pixhawk'],indicator_pixhawk)
		#print(send)
		#Send(bytearray(send,'utf-8'))
			
		#PixyLamp(command['pixyLight'])
	


		

















if __name__ == "__main__":
	try:
		print("Running...")
		while True:
			Run()
	except KeyboardInterrupt:
		CloseConnection()
	except Exception as e:
		camera1.EndStream()
		camera2.EndStream()
		print(e)

