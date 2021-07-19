import cv2 as cv
while True:
	cap = cv.VideoCapture("udpsrc port=9521 ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! decodebin ! videoconvert ! appsink", cv.CAP_GSTREAMER)

	if (cap.isOpened()== False):
		print("Error opening video stream or file")
	while (cap.isOpened()):
		ret, frame = cap.read()
		cv.imshow("TEST",frame)
		if cv.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv.destroyAllWindows()
