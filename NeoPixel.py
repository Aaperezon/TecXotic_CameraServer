from time import sleep
import board
import neopixel
import threading
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 16

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

thread_warning = None
end_thread = False

def wheel(pos):
	# Input a value 0 to 255 to get a color value.
	# The colours are a transition r - g - b - back to r.
	if pos < 0 or pos > 255:
		r = g = b = 0
	elif pos < 85:
		r = int(pos * 3)
		g = int(255 - pos * 3)
		b = 0
	elif pos < 170:
		pos -= 85
		r = int(255 - pos * 3)
		g = 0
		b = int(pos * 3)
	else:
		pos -= 170
		r = 0
		g = int(pos * 3)
		b = int(255 - pos * 3)
	return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
	for j in range(255):
		for i in range(num_pixels):
			pixel_index = (i * 256 // num_pixels) + j
			pixels[i] = wheel(pixel_index & 255)
		pixels.show()
		sleep(wait)

def SetColorRGB(r,g,b):
	pixels.fill((r,g,b))

def PutRGBColor(r,g,b,stateBtn):
	if(thread_warning == None):
		if(stateBtn == True):
			pixels.fill((r,g,b))
			pixels.show()
		elif(stateBtn == False):
			pixels.fill((0,0,0))
			pixels.show()

def WarningConnectionPixhawk(stop):
	while True:
		pixels.fill((255,51,0))
		pixels.show()
		sleep(.5) 
		pixels.fill((0,0,0))
		pixels.show()
		sleep(.5) 
		if(end_thread == True):
			break
def SuccessAllConnections(stop):
	global thread_warning
	for i in range(3):
		pixels.fill((0,255,0))
		pixels.show()
		sleep(.2) 
		pixels.fill((0,0,0))
		pixels.show()
		sleep(.2)
	thread_warning = None
def WarningConnectionUI(stop):
	while True:
		pixels.fill((255,0,0))
		pixels.show()
		sleep(.5) 
		pixels.fill((0,0,0))
		pixels.show()
		sleep(.5) 
		if (end_thread == True):
			break
def KillLightsThread():
	global end_thread, thread_warning
	if(end_thread == False):
		end_thread = True
	if(thread_warning != None):
		thread_warning.join()
	end_thread = False
	thread_warning = None
	SetColorRGB(0,0,0)

def AssignThread(function):
	global thread_warning, thread_exists
	thread_warning = threading.Thread(target = function, args = (lambda : end_thread,))
	thread_warning.start()

if __name__ == "__main__":

	try:
		while True:
			#rainbow_cycle(0.001)
			AssignThread(WarningConnectionUI)
			sleep(3)
			KillLightsThread()
			print("iniciando segundo thread")
			AssignThread(WarningConnectionPixhawk)
			sleep(3)
			KillLightsThread()
	except Exception as e:
		KillLightThread()
		print("LEDs turned off")
