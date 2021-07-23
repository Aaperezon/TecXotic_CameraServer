from RelayLEDs import *
#from NeoPixel import *
from time import sleep
import threading
thread_warning = None
end_thread = False



front_LED = RelayManager(2)
down_LED = RelayManager(3)
def WarningConnectionUI(stop):
	while True:
		front_LED.Switch(1)
		down_LED.Switch(1)
		sleep(.7)
		front_LED.Switch(0)
		down_LED.Switch(0)
		sleep(.7)
		if end_thread == True:
			break


def WarningConnectionPixhawk(stop):
	while True:
		front_LED.Switch(1)
		down_LED.Switch(0)
		sleep(.7)
		front_LED.Switch(0)
		down_LED.Switch(1)
		sleep(.7)
		if end_thread == True:
			break


def SuccessAllConnections(stop):
	front_LED.Switch(1)
	down_LED.Switch(1)
	sleep(2)
	front_LED.Switch(0)
	down_LED.Switch(0)
	thread_warning = None
def KillLightsThread():
	global end_thread, thread_warning
	if(end_thread == False):
		end_thread = True
	if(thread_warning != None):
		thread_warning.join()
	end_thread = False
	thread_warning = None
	front_LED.Switch(0)
	down_LED.Switch(0)

def AssignThread(function):
        global thread_warning, thread_exists
        thread_warning = threading.Thread(target = function, args = (lambda : end_thread,))
        thread_warning.start()
def GetLight1():
	return front_LED
def GetLight2():
	return down_LED


if __name__ == "__main__":
	try:
		AssignThread(WarningConnectionUI)
		sleep(3)
		KillLightsThread()
		print("iniciando segundo thread")
		AssignThread(WarningConnectionPixhawk)
		sleep(3)
		KillLightsThread()
		AssignThread(SuccessAllConnections)
	except Exception as e:
		print(e)
		KillLightThread()
		print("LEDs turned off")
