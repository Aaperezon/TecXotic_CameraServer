from ConnectionPixhawk import *
from ManualControl import *
from ConnectionUI import *

master = ConnectToPixhawk()
iter = 0

def request_message_interval(message_id, frequency_hz):
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        message_id, # The MAVLink message ID
        0, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
        0, 0, 0, 0)
request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_HEARTBEAT, 0)
def Run():
	global master,iter
	master.recv_match()
	a = False
	receive = Receive()
	if(receive != None):
		Arm_Disarm(master, bool(receive['arm_disarm']))
		
		if(iter > 0 and iter % 1000 == 0):
			Arm_Disarm(master, True)
			#master = Arm_Disarm(master, True)
			a = True
		else:
			Arm_Disarm(master, False)
			a = False
		iter = iter +1
		if (iter < 1500):
			#print("Boton: "+str(receive['arm_disarm'])+"  "+str(iter)+"  Armed: "+str(bool(master.motors_armed()))+"   "+str(master.messages['ATTITUDE']))
			print("Boton: "+str(receive['arm_disarm'])+"  "+str(iter)+"  Armed: "+str(bool(master.motors_armed()))+"   ")






if __name__ == "__main__":
	try:
		print("Running...")
		while True:
			Run()
	except KeyboardInterrupt:
		print("Keyboard, nothing to do.")
	except Exception as e:
		print(e)
