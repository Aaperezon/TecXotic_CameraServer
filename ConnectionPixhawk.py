# Import mavutil
from pymavlink import mavutil

def ConnectToPixhawk():
	# Create the connection
	master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_Pixhawk1_2D0025001351383131383231-if00")
	#master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
	#master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_PH4-mini_3D001E001351383137383335-if00")
	
	# Wait a heartbeat before sending commands
	master.wait_heartbeat()
	return master



connection_pixhawk_changer = False
masterReturn = None
def ConnectDisconnectPixhawk(stateBtn):
	global connection_pixhawk_changer, masterReturn
	if(connection_pixhawk_changer == True and stateBtn == True and masterReturn == None):
		connection_pixhawk_changer = False
		masterReturn = ConnectToPixhawk()
		return masterReturn
	elif(connection_pixhawk_changer == False and stateBtn == False ):
		connection_pixhawk_changer = True
		masterReturn = None
		return masterReturn
	else:
		return masterReturn
