<<<<<<< HEAD

=======
>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4
from ConnectionUI import *
from ConnectionPixhawk import *
from ManualControl import *
from ServoManager import ServoManager
from ManualControlMiniROV import *
<<<<<<< HEAD
#from CameraStream import *
import Agent1Manager
#from HumidityTemperature import GetHumidityTemperature
import cv2 as cv
import base64
=======
from CameraStream import *
import Agent1Manager
#from HumidityTemperature import GetHumidityTemperature
>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4
indicator_pixhawk = False
indicator_pitch_camera=0


pixhawk_status = False
master = None
<<<<<<< HEAD

#cap = cv.VideoCapture(2)
#cap = cv.VideoCapture(camera1.GetStreamPipeline(), cv.CAP_GSTREAMER)
#cap = cv.VideoCapture("udpsrc port=9897 ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink",cv.CAP_GSTREAMER)
pitch_servo = ServoManager(17, min_angle=-60, max_angle=20)
#yaw_servo = ServoManager(27, min_angle=-40, max_angle=40)

=======
camera1 = CameraStream('0')
camera2 = CameraStream('2')
camera1.Run()
camera2.Run()
camera1_image = camera1.GetStream()
camera2_image = camera2.GetStream()
pitch_servo = ServoManager(17, min_angle=-60, max_angle=20)
yaw_servo = ServoManager(27, min_angle=-40, max_angle=40)
setup = False
>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4
pixhawk_indicator_LED = False
def Control(arm_disarm, roll, pitch, yaw, throttle, flight_mode, connect_pixhawk, r_LED,g_LED,b_LED, light1, light2):
	global indicator_pixhawk, pixhawkWarning, master, pixhawk_indicator_LED
	if(master != None):
		master.recv_match()
		pixhawk_indicator_LED = False

		Arm_Disarm(master, arm_disarm)
		Move(master, roll, pitch, yaw, throttle, 0)
		ChangeFlightMode(master, flight_mode)
		master = ConnectDisconnectPixhawk(connect_pixhawk)
		if (indicator_pixhawk == False):
			LightsManager.KillLightsThread()
			LightsManager.AssignThread(LightsManager.SuccessAllConnections)
			indicator_pixhawk = True
		else:
			LightsManager.GetLight1().Switch(light1)
			LightsManager.GetLight2().Switch(light2)
			pixhawk_indicator_LED = True

	else:
		indicator_pixhawk = False
		master = ConnectDisconnectPixhawk(connect_pixhawk)
		if pixhawk_indicator_LED == False:
			LightsManager.KillLightsThread()
			LightsManager.AssignThread(LightsManager.WarningConnectionPixhawk)
			pixhawk_indicator_LED = True

def UtilityControl(pitch_camera,yaw_camera,miniROV_direction,reel_direction,cam_port1, cam_port2):
	global indicator_pitch_camera
	pitch_servo.MoveServo(pitch_camera, 1)
<<<<<<< HEAD
	#yaw_servo.MoveServo(yaw_camera, 1)
	MoveMiniROV(miniROV_direction)
	MoveReel(reel_direction)
	
	
pipeline = "udpsrc port=7896 ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! decodebin ! videoconvert ! appsink"

def Run():
    global pixhawk_status,setup
    
    commands = Receive()
    if(commands != None):
        if commands['activate_agent1'] == True:
            #Agent1Manager.SetThrottle(commands['kp_throttle'], commands['ki_throttle'],commands['kd_throttle'],0)
            #Agent1Manager.SetRoll(commands['kp_roll'], commands['ki_roll'],commands['kd_roll'],0)
            #Agent1Manager.SetPitch(commands['kp_pitch'], commands['ki_pitch'],commands['kd_pitch'],0)
            #Agent1Manager.SetYaw(commands['kp_yaw'], commands['ki_yaw'],commands['kd_yaw'],0)
            Agent1Manager.SetThrottle(4, 3,1,0)     
            Agent1Manager.SetRoll(4, 3,1,0)
            Agent1Manager.SetPitch(4, 3,1,0)
            Agent1Manager.SetYaw(4, 3,1,0)
            Agent1Manager.Start(True, commands['cam_port1'])
              
        if commands['activate_agent1'] == False and commands['activate_agent2'] == False and commands['activate_agent3'] == False:
            Agent1Manager.Start(False, None)
            Control(commands['arm_disarm'],commands['roll'],commands['pitch'],commands['yaw'],commands['throttle'], commands['flight_mode'], commands['connect_pixhawk'], commands['r_LED'],commands['g_LED'],commands['b_LED'],commands['light1'], commands['light2'])
            UtilityControl(commands['pitch_camera'],commands['yaw_camera'], commands['miniROV_direction'],commands['reel_direction'],commands['cam_port1'],commands['cam_port2'])
	        #hum, temp = GetHumidityTemperature()
        
        
        hum, temp = (0,0)
        
        send = {
=======
	yaw_servo.MoveServo(yaw_camera, 1)
	MoveMiniROV(miniROV_direction)
	MoveReel(reel_direction)
	camera1.SaveCameraPort(int(cam_port1))
	camera2.SaveCameraPort(int(cam_port2))
def Run():
	global pixhawk_status,setup
	commands = Receive()
	if(commands != None):
		if commands['activate_agent1'] == True and setup == False:
			Agent1Manager.Setup(commands['kp_pitch'], commands['ki_pitch'],commands['kd_pitch'],0)
			setup = True
		elif commands['activate_agent1'] == False:
			setup = False

		Agent1Manager.Run(commands['activate_agent1'], camera1_image)
		#print(str(commands))
		Control(commands['arm_disarm'],commands['roll'],commands['pitch'],commands['yaw'],commands['throttle'], commands['flight_mode'], 
			commands['connect_pixhawk'], commands['r_LED'],commands['g_LED'],commands['b_LED'],commands['light1'], commands['light2'])
		UtilityControl(commands['pitch_camera'],commands['yaw_camera'], commands['miniROV_direction'],commands['reel_direction'],commands['cam_port1'],commands['cam_port2'])
		#hum, temp = GetHumidityTemperature()
		hum, temp = (0,0)
		send = {
>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4
				"connection_pixhawk": indicator_pixhawk,
				"pitch_camera" : indicator_pitch_camera,
				"pressure":0,
	        		"clamp": False,
				"light": False,
				"throttle":commands['throttle'],
				"roll":commands['roll'],
				"pitch":commands['pitch'],
				"yaw":commands['yaw'],
				"temperature": hum,
				"humidity": temp,
<<<<<<< HEAD
				"camera1_showing": False, #bool(camera1_image),
				"camera2_showing": False,
				#"image": base64.b64encode(a).decode("utf-8")
				
				
		       }

        send = json.dumps(send)
        send = str(send)
        #print(commands['connect_pixhawk'],indicator_pixhawk)

        Send(bytearray(send,'utf-8'))
        
=======
				"camera1_showing": bool(camera1_image),
				"camera2_showing": False
		       }
		send = json.dumps(send)
		send = str(send)
		#print(commands['connect_pixhawk'],indicator_pixhawk)
		#print(send)
		Send(bytearray(send,'utf-8'))











>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4






if __name__ == "__main__":
<<<<<<< HEAD
    try:
        print("Running...")
        while True:
            Run()
    except KeyboardInterrupt:
        CloseConnection()
       
    except Exception as e:
        #camera1.EndStream()
        #camera2.EndStream()
        #LightsManager.KillLightsThread()
        print(e)

      
=======
	try:
		print("Running...")
		while True:
			Run()
	except KeyboardInterrupt:
		CloseConnection()
	except Exception as e:
		camera1.EndStream()
		#camera2.EndStream()
		#LightsManager.KillLightsThread()
		print(e)
		#blue_light.Switch(0)

>>>>>>> 51d663e401fe4c3504227dbbd88eefda401ae5e4
