from threading import Thread
from time import sleep
import gi

gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib


Gst.init()

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

pipeline = Gst.parse_launch("v4l2src device=/dev/video0 do-timestamp=true ! queue ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.2.1 port=5656")

pipeline.set_state(Gst.State.PLAYING)

try:
	while True:
		sleep(.1)
except KeyboardInterrupt:
	pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()
