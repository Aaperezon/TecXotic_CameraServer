from gpiozero import AngularServo
from time import sleep
from threading import Thread

MAX_angle = 44
MIN_angle = -42
pitch_angle = MIN_angle
pitch_servo = AngularServo(17, min_angle=MIN_angle, max_angle=MAX_angle)

thread_servo = None
end_thread = False

pitch_servo.angle = MIN_angle


def MoveMainCamera(direction, speed):
	global pitch_angle
	if direction == 'u':
		pitch_servo.angle = pitch_angle + speed
	elif direction == 'd':
		pitch_servo.angle = pitch_angle - speed
	return pitch_servo.angle


def AssignThread(function,direction,speed):
	global thread_servo
	thread_servo = Thread(target=function, args = (direction,speed))
	thread_servo.start()



if __name__ == "__main__":
	try:
		AssignThread(MoveMainCamera,'u',10) 
	except Exception as e:
		print(e)

