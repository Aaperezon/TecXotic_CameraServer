# Import mavutil
from pymavlink import mavutil

def ConnectToPixhawk():
	# Create the connection
	#master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_Pixhawk1-1M_2D0025001351383131383231-if00")
	master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
	#master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_PH4-mini_3D001E001351383137383335-if00")
	
	# Wait a heartbeat before sending commands
	master.wait_heartbeat()
	return master



connection_pixhawk_changer = False

def ConnectDisconnectPixhawk(stateBtn):
	global arm_disarm_changer
	if(connection_pixhawk_changer == True and stateBtn == True):
		arm_disarm_changer = False
		return ConnectToPixhawk()
	elif(connection_pixhawk_changer == False and stateBtn == False):
		arm_disarm_changer = True
		return None
