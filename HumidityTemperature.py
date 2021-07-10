import board
import Adafruit_DHT

class HumidityTemperature:
	def __init__(self, pin):
		self.pin = pin
		self.temp = 0
		self.hum = 0
	def GetData(self):
		humidity, temperature = Adafruit_DHT.read(11, self.pin)
		if humidity != None and temperature != None:
			self.temp = temperature
			self.hum = humidity
		return self.hum, self.temp

if __name__ == "__main__":
	
	sensor = HumidityTemperature(25)
	try:
		while True:
			temp, hum = sensor.GetData()
			print(f"humedad: {temp} temperatura: {hum}")
		
	except Exception as e:
		print(e)
