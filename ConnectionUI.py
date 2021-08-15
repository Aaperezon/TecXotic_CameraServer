import socket
import json
TCP_IP = '127.0.0.1'
TCP_PORT = 55000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
	global conectionAllowed
	if(conectionAllowed == True):
		received = conn.recv(BUFFER_SIZE)
		if not received: 
			print("Data error...")
			conn.close()
			conectionAllowed = False
		try:
			print(f"Real Received {received}")
			received = received.decode("utf-8")
			received = "{}".format(received)
			received = json.loads(received)
			return received
		except:
			#conn.close()
			pass
	else:
		print("Waiting for client...")
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



if __name__ == "__main__":
	try:
		print("Running...")
		while True:
			commands = Receive()
			if commands != None:
				print("Received")
				print(str(commands))
			else:
				print("No commands")
	except KeyboardInterrupt:
		CloseConnection()
	except Exception as e:
		print(e)

      
