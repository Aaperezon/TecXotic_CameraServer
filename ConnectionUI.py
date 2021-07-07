import socket
import json
import  LightsManager
TCP_IP = '192.168.2.2'
TCP_PORT = 55000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conectionAllowed = False

conn = None
addr = None

UI_indicator_LED = False
pixhawk_indicator_LED = False
def ConnectTo():
	global conn,addr,conectionAllowed
	conn, addr = s.accept()
	print ('Connection address:', addr)
	conectionAllowed = True
	print ("Connection success...")
	
def Receive():
	global conectionAllowed, LEDSuccess,LEDPixhawkWarning,LEDClientWarning,UI_indicator_LED, pixhawk_indicator_LED
	if(conectionAllowed == True):
		received = conn.recv(BUFFER_SIZE)
		if not received: 
			print("Error de datos")
			conn.close()
			conectionAllowed = False
		try:
			#Decodification here
			received = received.decode("utf-8")
			received = "{}".format(received)
			received = json.loads(received)
			return received
		except:
			#conn.close()
			pass
	else:
		print("Waiting for client...")
		if UI_indicator_LED == True:
			LightsManager.KillLightsThread()
			LightsManager.AssignThread(LightsManager.WarningConnectionUI)
			UI_indicator_LED = False
		ConnectTo()
	
def CloseConnection():
	global conn
	try:
		conn.close()
	except Exception as e: 
		print(e)

	print("Closed connection...")

def Send(data):
	if(conectionAllowed == True):
		try:
			conn.sendall(data)
		except Exception as e:
			print(e)	
