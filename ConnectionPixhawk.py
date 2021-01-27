# Import mavutil
from pymavlink import mavutil

def ConnectToPixhawk():
	# Create the connection
	master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
	# Wait a heartbeat before sending commands
	master.wait_heartbeat()
	return master
