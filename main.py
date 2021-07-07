from ConnectionUI import *
from ConnectionPixhawk import *
from ManualControl import *
from ServoManager import ServoManager
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
pitch_servo = ServoManager(17)
yaw_servo = ServoManager(27)
pixhawk_indicator_LED = True
def Control(arm_disarm, roll, pitch, yaw, throttle, flight_mode, connect_pixhawk, r_LED,g_LED,b_LED, light):
	global indicator_pixhawk, pixhawkWarning, master, pixhawk_indicator_LED
	if(master != None):
		master.recv_match()
		Arm_Disarm(master, arm_disarm)
		Move(master, roll, pitch, yaw, throttle, 0)
		ChangeFlightMode(master, flight_mode)
		master = ConnectDisconnectPixhawk(connect_pixhawk)
		if (indicator_pixhawk == False):
			LightsManager.KillLightsThread()
			LightsManager.AssignThread(LightsManager.SuccessAllConnections)
			indicator_pixhawk = True
		else:
			LightsManager.PutRGBColor(r_LED,g_LED,b_LED, light)
			pixhawk_indicator_LED = True

	else:
		indicator_pixhawk = False
		master = ConnectDisconnectPixhawk(connect_pixhawk)
		if pixhawk_indicator_LED == True:
			LightsManager.KillLightsThread()
			LightsManager.AssignThread(LightsManager.WarningConnectionPixhawk)
			pixhawk_indicator_LED = False
		UI_indicator_LED = True

def UtilityControl(pitch_camera,yaw_camera,miniROV_direction,cam_port1, cam_port2):
	global indicator_pitch_camera
	pitch_servo.MoveServo(pitch_camera, 1)
	yaw_servo.MoveServo(yaw_camera, 1)
	#MoveMiniROV(miniROV_direction)
	camera1.SaveCameraPort(int(cam_port1))
	camera2.SaveCameraPort(int(cam_port2))
def Run():
	global pixhawk_status
	commands = Receive()
	if(commands != None):
		print(str(commands))
		Control(commands['arm_disarm'],commands['roll'],commands['pitch'],commands['yaw'],commands['throttle'], commands['flight_mode'], 
			commands['connect_pixhawk'], commands['r_LED'],commands['g_LED'],commands['b_LED'],commands['light'])
		UtilityControl(commands['pitch_camera'],commands['yaw_camera'], commands['miniROV_direction'],commands['cam_port1'],commands['cam_port2'])

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
		Send(bytearray(send,'utf-8'))
			
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
		LightsManager.KillLightsThread()
		print(e)

