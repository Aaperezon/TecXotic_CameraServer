import socket
import json
import time
from json.decoder import JSONDecodeError

TCP_IP = 'raspberrypi.local'
TCP_PORT = 55000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

def Run(s):
    while 1:
        conn, addr = s.accept()
        print ('Connection address:', addr)
        while 1:
            received = conn.recv(BUFFER_SIZE)
            if not received: break
            try:
                #All my logic and implementations here
                received = received.decode("utf-8")
                received = "{}".format(received)
                received = json.loads(received)
                print(received["show_hide"])
            except JSONDecodeError as e:
                #conn.close()
                pass
        print("Connection closed from client")            
        
def Start():
    global conn, addr, s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    Run(s)
       
    
if __name__ == "__main__":
    Start()
