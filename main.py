from Connection import *
#from pixycam import *

while True:
    if(Receive() == True):
        command = GetReceivedData()
        print(command)
        #PixyLamp(command['pixyLight'])
