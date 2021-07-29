import socket
import json
import CameraStream
TCP_IP = '192.168.2.2'
TCP_PORT = 56000
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
			print("Error de datos")
			conn.close()
			conectionAllowed = False
			UI_indicator_LED = False
		try:
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
			
			
	
	
camera1 = CameraStream.CameraStream('0')		
camera2 = CameraStream.CameraStream('2')

		
def Run():
    commands = Receive()
    if(commands != None):
        #print(str(commands))
        camera1.SaveCameraPort(int(commands['cam_index1']),int(commands['cam_port1']))        
        camera2.SaveCameraPort(int(commands['cam_index2']),int(commands['cam_port2']))

   


if __name__ == "__main__":
    try:
        print("Running Camera Server...")
        camera1.Run()
        camera2.Run()
        while True:
            Run()
    except KeyboardInterrupt:
        CloseConnection()
    except Exception as e:
        print(e)

