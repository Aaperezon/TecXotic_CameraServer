import socket
import json
import time
from json.decoder import JSONDecodeError
from pixycam import *
TCP_IP = 'raspberrypi.local'
TCP_PORT = 55000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conectionAllowed = False
receivedData = ''
def ConnectTo():
    global s,conn,conectionAllowed
    conn, addr = s.accept()
    print ('Connection address:', addr)
    conectionAllowed = True

def Receive():
    global conn,conectionAllowed,receivedData
    if(conectionAllowed == True):
        received = conn.recv(BUFFER_SIZE)
        if not received: 
            print("Error de datos")
            conn.close()
            conectionAllowed = False
        try:
            #All my logic and implementations here
            received = received.decode("utf-8")
            received = "{}".format(received)
            received = json.loads(received)
            receivedData = received
            return True
            #PixyLamp(received["pixyLight"])
        except:
            #conn.close()
            pass
       
    else:
        ConnectTo()


def GetReceivedData():
    global receivedData
    return receivedData
