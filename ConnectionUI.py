import socket
import json
#import  LightsManager
TCP_IP = '192.168.2.4'
TCP_PORT = 55000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conectionAllowed = False

conn = None
addr = None
def ConnectTo():
	global conn,addr,conectionAllowed
	conn, addr = s.accept()
	print ('Connection address:', addr)
	conectionAllowed = True
	print ("Connection success...")
	
def Receive():
	global conectionAllowed, LEDSuccess,LEDPixhawkWarning,LEDClientWarning
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
		#LightsManager.KillThread()
		#LightsManager.AssignThread(LightsManager.WarningConnectionUI)
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
