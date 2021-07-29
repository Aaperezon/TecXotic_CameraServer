from threading import Thread
import cv2 as cv
from time import sleep
import gi
import sys
import json
import os.path
gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib

class CameraStream:
    def __init__(self,camera_index):
        self.main_thread = None
        self.camera_index = camera_index
        self.camera_port = None
        self.main_loop = None
        self.main_loop_thread = None
        self.pipeline = ""
        self.cap = None
    def SaveCameraPort(self,new_device, new_port):
	    if self.camera_port == new_port and self.camera_index == new_device:
		    return
	    camera_settings_read_file = open('./Source/CameraSettings.json', "r")
	    camera_settings_read = json.loads(camera_settings_read_file.read())
	    camera_settings_read_file.close()
	    self.camera_index = new_device
	    camera_settings_read[str(self.camera_index)] = new_port
	    camera_settings_write_file = open('./Source/CameraSettings.json',"w")
	    json.dump(camera_settings_read, camera_settings_write_file)
	    camera_settings_write_file.close()
	    self.camera_port = new_port
	    self.EndStream()
	    self.Run()
    def LoadCameraPort(self):
	    PATH = ("./Source/CameraSettings.json")
	    if not os.path.isfile(PATH):
		    DEFAULT_DATA = {
			    '0': 5656,
			    '1': 5700,
			    '2': 5657,
			    '3': 7894,
			    '4': 9890
		    }
		    os.makedirs(os.path.dirname(PATH), exist_ok=True)
		    DEFAULT_FILE = open(PATH, 'w')
		    json.dump(DEFAULT_DATA, DEFAULT_FILE)
		    self.camera_port = DEFAULT_DATA[self.camera_index]
		    return self.camera_port
	    else:
		    camera_settings_file = open (PATH, 'r')
		    camera_settings = json.loads(camera_settings_file.read())
		    self.camera_port = camera_settings[str(self.camera_index)]
		    return self.camera_port
    def Run(self):
	    self.LoadCameraPort()
	    Gst.init()
	    self.main_loop = GLib.MainLoop()
	    self.main_loop_thread = Thread(target=self.main_loop.run, daemon=True)
	    self.main_loop_thread.start()
	    self.pipeline = Gst.parse_launch("v4l2src device=/dev/video"+str(self.camera_index)+" ! video/x-raw,width=320,height=240 ! queue ! jpegenc ! rtpjpegpay ! multiudpsink clients=192.168.2.1:"+str(self.camera_port)+",192.168.2.2:"+str(self.camera_port+1))
	    self.pipeline.set_state(Gst.State.PLAYING)
	    print(f"new stream is video{self.camera_index} on: {self.camera_port}")
   
   
   
    def GetStreamPipeline(self):
	    return "udpsrc port="+str(self.camera_port+1)+" ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! decodebin ! videoconvert ! appsink" 
	    #self.cap = cv.VideoCapture("udpsrc port="+str(self.camera_port+1)+" ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! decodebin ! videoconvert ! appsink", cv.CAP_GSTREAMER)

   
    def EndStream(self):
	    #self.cap.release()
	    self.pipeline.set_state(Gst.State.NULL)
	    self.main_loop.quit()
	    self.main_loop_thread.join()
	    
	    
if __name__ == "__main__":
    import cv2 as cv
    camera1 = CameraStream('0')
    try:
        camera1.Run()
        while True:
            print("running camera...")
    except KeyboardInterrupt:
        camera1.EndStream()
