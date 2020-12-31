from __future__ import print_function
from pixyModules import pixy
from ctypes import *
from pixyModules import *
# Pixy2 Python SWIG Set Lamp Example #

print("Pixy2 Python SWIG Example -- Set Lamp")

pixy.init ()
pixy.change_prog ("video")

stateOn = False
stateOff = False
def PixyLamp(state):
    global stateOff, stateOn
    if(stateOn):
        pixy.set_lamp (1,0)
    else:
        pixy.set_lamp (0,0)
    if (state == True):
        if (not stateOff):
            stateOn = not stateOn
            stateOff = True
    else:
        stateOff = False
"""
#Para pruebas con este mismo archivo
while True:
    a = input("Estado: ")
    PixyLamp(a)
"""