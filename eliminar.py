from gpiozero import Servo,AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

pitch_servo = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
MAX_angle = 90
MIN_angle = -90
pitch_angle = MIN_angle
thread_servo = None
end_thread = False

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def SetAngle(servo, angle):
        angle = remap(angle, MIN_angle, MAX_angle, -1, 1)
        servo.value = angle
def MoveMainCamera(direction, speed):
        global pitch_angle
        if direction == 'u' and pitch_angle < MAX_angle:
                SetAngle(pitch_servo, pitch_angle + speed)
                pitch_angle = pitch_angle + speed
        elif direction == 'd' and pitch_angle > MIN_angle:
                SetAngle(pitch_servo, pitch_angle - speed)
                pitch_angle = pitch_angle - speed

def GetPitchAngle():
        return pitch_angle
SetAngle(pitch_servo,pitch_angle)
if __name__ == "__main__":
        try:
                while True:
                        instruction = input("u, d : ")
                        MoveMainCamera(instruction,1)

                        print(GetPitchAngle())
        except Exception as e:
                print(e)
