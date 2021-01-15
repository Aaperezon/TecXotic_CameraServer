from Connection import *
#from pixycam import *



def Run():
	if(Receive() == True):
		command = GetReceivedData()
		print(command)
		Send(b"Hola esta es una prueba")
			
		#PixyLamp(command['pixyLight'])

if __name__ == "__main__":
	try:
		print("Running...")
		while True:
			Run()
	except KeyboardInterrupt:
		CloseConnection()
	except Exception as e:
		print(e)

