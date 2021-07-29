#from RelayLEDs import *
#from NeoPixel import *
from SolidStateRelay import *

from time import sleep
import threading
thread_warning = None
end_thread = False



down_LED = SolidStateRelay(3)
warning_LED = SolidStateRelay(4)
def WarningConnectionUI(stop):
	while True:
		warning_LED.Switch(1)
		sleep(.7)
		warning_LED.Switch(0)
		sleep(.7)
		if end_thread == True:
			break


def WarningConnectionPixhawk(stop):
	while True:
		warning_LED.Switch(1)
		sleep(.3)
		warning_LED.Switch(0)
		sleep(.3)
		if end_thread == True:
			break


def SuccessAllConnections(stop):
	warning_LED.Switch(1)
	sleep(2)
	warning_LED.Switch(0)
	thread_warning = None
def KillLightsThread():
	global end_thread, thread_warning
	if(end_thread == False):
		end_thread = True
	if(thread_warning != None):
		thread_warning.join()
	end_thread = False
	thread_warning = None
	warning_LED.Switch(0)

def AssignThread(function):
        global thread_warning
        thread_warning = threading.Thread(target = function, args = (lambda : end_thread,))
        thread_warning.start()
def GetLight1():
	return down_LED
def GetLight2():
	return warning_LED

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
