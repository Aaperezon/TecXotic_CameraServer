from __future__ import print_function
from pixy2.build.python_demos import pixy
from ctypes import *
from pixy2.build.python_demos.pixy import *
import json
# Pixy2 Python SWIG Set Lamp Example #

print("Pixy2 Python SWIG Example -- Set Lamp")

pixy.init ()
pixy.change_prog ("color_connected_components")

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




class Blocks (Structure):
	_fields_ = [ ("m_signature", c_uint),
	("m_x", c_uint),
	("m_y", c_uint),
	("m_width", c_uint),
	("m_height", c_uint),
	("m_angle", c_uint),
	("m_index", c_uint),
	("m_age", c_uint) ]

blocks = BlockArray(1)

def GetPixyTarget():
	count = pixy.ccc_get_blocks(1, blocks)
	if count > 0:
		retorno = {"target_x":'%3d'%blocks[0].m_x,"target_y":"%3d"%blocks[0].m_y,"target_width":"%3d"%blocks[0].m_width,"target_height":"%3d"%blocks[0].m_height}
		retorno['target_x'] = int(retorno['target_x'])
		retorno['target_y'] = int(retorno['target_y'])
		retorno['target_width'] = int(retorno['target_width'])
		retorno['target_height'] = int(retorno['target_height'])
		retorno = json.dumps(retorno)
		return str(retorno)
	else:
		retorno = {"target_x":0,"target_y":0,"target_width":0,"target_height":0}
		retorno = json.dumps(retorno)
		return str(retorno)
		



"""
while 1:
	print(GetPixyTarget())


#Para pruebas con este mismo archivo
while True:
    a = input("Estado: ")
    PixyLamp(a)
"""
