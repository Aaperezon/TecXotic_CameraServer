
import cv2 as cv
import numpy as np
import PID
import json


cap = None
camera_port1 = None
def Initialize():
	global cap, camera_port1
	PATH = ("./Source/CameraSettings.json")
	camera_settings_file = open (PATH, 'r')
	camera_settings = json.loads(camera_settings_file.read())
	camera_port1 = int(camera_settings[str(0)]+1)
	cap = cv.VideoCapture("udpsrc port="+str(camera_port1)+" ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! decodebin ! videoconvert ! appsink", cv.CAP_GSTREAMER)
def CreateMask(img, hsv_low, hsv_high ):
    # img = img.copy()
    hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV) #cambiar la imagen de BGR a HSV
    hsvImg = cv.medianBlur(hsvImg,3)   #elimina el ruido opacando la imagen
    color_low = np.array([hsv_low[0], hsv_low[1], hsv_low[2]], np.uint8)
    color_high = np.array([hsv_high[0], hsv_high[1], hsv_high[2]], np.uint8)
    color_mask = cv.inRange(hsvImg, color_low, color_high)  #crea la mascara para el color
    return color_mask




def Run():
	turn = throttle = 0
	if (cap.isOpened()== False):
		print("Error opening video stream or file")
	if (cap.isOpened()):
		ret, frame = cap.read()
		size = np.shape(frame)[0:2]
		frame_mask = CreateMask(frame, (18,83,101) , (51,192,205))
		contours, hierarchy = cv.findContours(frame_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
		contours = sorted(contours, key=cv.contourArea, reverse=True)
		contour = contours[0]
		rect = cv.minAreaRect(contour)
		box = cv.boxPoints(rect)
		box = np.int0(box)
		cv.drawContours(frame,[box],-1,(0,255,0),3)
		#cv.circle(frame, tuple(box[0]), 5, (255,0,0), 4 )
		#cv.circle(frame, tuple(box[2]), 5, (0,255,0), 4 )
		pointX = pointY = 0
		pointX = int(box[0][0] + (box[2][0] - box[0][0])/2)
		if box[0][1] < box[2][1]:
			pointY = int(box[0][1] + (box[2][1] - box[0][1])/2)
		else:
			pointY = int(box[2][1] + (box[0][1] - box[2][1])/2)
		cv.circle(frame, (pointX, pointY), 5, (0,0,255), 10 )
		turn = int(pointX - (size[1]/2))
		throttle = -int(pointY - (size[0]/2))
		print(f"turn: {turn}  throttle: {throttle}")

		#cv.imshow('Video',frame)
	return turn


if __name__ == "__main__":
        
        try:
                while True:
			pass
        except Exception as e:
                print(e)


