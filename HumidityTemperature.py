import board
import Adafruit_DHT
from threading import Thread
import time
temp = 0
hum = 0
pin = 25


def GetHumidityTemperature():
	global temp, hum
	humidity, temperature = Adafruit_DHT.read(11, pin)
	if humidity != None and temperature != None:
		temp = temperature
		hum = humidity
	return hum, temp
def Start():
	while True:
		print(f"LSKDNLNFNWFNWKEJNÑWJNDNCÑWJ NCÑWKJ DCÑKWJ CÑKWJECJNEÑWNWÑEN")
		time.sleep(4)
def StartThread():
	thread = Thread(target = Start)
	thread.start()








if __name__ == "__main__":
	#StartThread()
	try:
		while True:
			hum,temp = GetHumidityTemperature()
			print(f"humedad: {temp} temperatura: {hum}")
		
	except Exception as e:
		print(e)
