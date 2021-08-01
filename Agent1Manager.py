import Agent1Test
import PID
import cv2 as cv
#import LightsManager
a = 2
kP_throttle = a
kI_throttle = 0
kD_throttle = 0
throttle_target = 0
pid_throttle = PID.PID(kP_throttle,kI_throttle,kD_throttle)

kP_roll = a
kI_roll = 0
kD_roll = 0
roll_target = 0
pid_roll = PID.PID(kP_roll,kI_roll,kD_roll)

kP_pitch = a
kI_pitch = 0
kD_pitch = 0
pitch_target = 0 
pid_pitch = PID.PID(kP_pitch,kI_pitch,kD_pitch)

kP_yaw = a
kI_yaw = 0
kD_yaw = 0
yaw_target = 0
pid_yaw = PID.PID(kP_yaw,kI_yaw,kD_yaw)


def GetThrottlePID():
    return pid_throttle
def GetRollPID():
    return pid_roll
def GetPitchPID():
    return pid_pitch
def GetYawPID():
    return pid_yaw



def SetThrottle(kP, kI, kD, target):
    global  kP_throttle, kI_throttle, kD_throttle, throttle_target
    if kP != kP_throttle or kI != kI_throttle or kD != kD_throttle or target != throttle_target:
        pid_throttle.SetPoint = target
        pid_throttle.setKp(kP)
        pid_throttle.setKi(kI)
        pid_throttle.setKd(kD)

def SetRoll(kP, kI, kD, target):
    global  kP_roll, kI_roll, kD_roll, roll_target
    if kP != kP_roll or kI != kI_roll or kD != kD_roll or target != roll_target:
        pid_roll.SetPoint = target
        pid_roll.setKp(kP)
        pid_roll.setKi(kI)
        pid_roll.setKd(kD)

def SetPitch(kP, kI, kD, target):
    global  kP_pitch, kI_pitch, kD_pitch, pitch_target
    if kP != kP_pitch or kI != kI_pitch or kD != kD_pitch or target != pitch_target:
        pid_pitch.SetPoint = target
        pid_pitch.setKp(kP)
        pid_pitch.setKi(kI)
        pid_pitch.setKd(kD)


def SetYaw(kP, kI, kD, target):
    global  kP_yaw, kI_yaw, kD_yaw, yaw_target
    if kP != kP_yaw or kI != kI_yaw or kD != kD_yaw or target != yaw_target:
        pid_yaw.SetPoint = target
        pid_yaw.setKp(kP)
        pid_yaw.setKi(kI)
        pid_yaw.setKd(kD)

cap = None
def Start(activate, port):
    global cap
    throttle = roll = pitch = yaw = 0
    if activate == True:
        if cap == None:
            cap = cv.VideoCapture("udpsrc port="+str(port)+" ! application/x-rtp,encodingname=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! decodebin ! videoconvert ! appsink", cv.CAP_GSTREAMER)
            #cap = cv.VideoCapture("prueba2.wmv")
        if cap.isOpened():
            ret,frame = cap.read()
            frame = cv.resize(frame, (320,240))
            throttle, roll, pitch, yaw = Agent1Test.Start(frame)
            pid_throttle.update(throttle)
            pid_roll.update(roll)
            pid_pitch.update(pitch)
            pid_yaw.update(yaw)
            throttle = pid_throttle.output
            roll = pid_roll.output
            pitch = pid_pitch.output
            yaw = pid_yaw.output
            print(f"""
            throttle:  { pid_throttle.output - 500}
            roll: { pid_roll.output }
            pitch : { pid_pitch.output }
            yaw : { pid_yaw.output }
             """)
            if cv.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv.destroyAllWindows()
    else:
        cap = None

    return int(throttle), int(roll), int(pitch), int(yaw)






 
if __name__ == "__main__":
    try:
        #cap = cv.VideoCapture("prueba2.wmv")

        #LightsManager.GetLight1().Switch(1)
        while True:
	        if cap.isOpened():
		        ret, frame = cap.read()
		        frame = cv.resize(frame, (640,480))
		        Start(True, frame)
		        if cv.waitKey(25) & 0xFF == ord('q'):
			        break
        cap.release()
        cv.destroyAllWindows()
    except:
	    cap.release()
	    cv.destroyAllWindows()
