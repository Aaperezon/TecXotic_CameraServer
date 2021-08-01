import cv2 as cv
import numpy as np
import math


throttle = roll = pitch = yaw = 0

def Start(frame):
    global throttle, roll, pitch, yaw
    #frame = cv.imread('./test_line1.png')  #Single image, already cropped
    frame = cv.GaussianBlur(frame,(5,5),0)
    #hsvImg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsvImg = frame
    cv.imshow("HSV Image",hsvImg)
    hsvImg = hsvImg[:,:,2]

    cv.imshow("one channel",hsvImg)


    hsvImg = cv.applyColorMap(hsvImg, cv.COLORMAP_OCEAN)
    cv.imshow("ocean c1",hsvImg)
    hsvImg = cv.applyColorMap(hsvImg, cv.COLORMAP_HSV)
    #hsvImg = cv.cvtColor(hsvImg, cv.COLOR_BGR2HSV)

    cv.imshow("ocean colormap",hsvImg)
    #hsvImg = cv.cvtColor(hsvImg, cv.COLOR_BGR2HSV)
    #cv.imshow("color for mask",hsvImg)

    color_low = np.array([0,40,0], np.uint8)
    color_high = np.array([180,50,255], np.uint8)
    result = cv.inRange(hsvImg, color_low,color_high)
    cv.imshow("first mask",result)

    kernel = np.ones((3,3), np.uint8)
    result = cv.dilate(result, kernel, iterations=4)
    cv.imshow("dilate",hsvImg)

    edged = cv.Canny(result,threshold1=0, threshold2=0)
    cv.imshow("Edged",edged)

    lines = cv.HoughLines(edged, rho=1, theta=np.pi/180, threshold=50, lines=None,srn=0,stn=0)
    line1 = None
    line2 = None
    if lines is not None:
        if len(lines) >= 2:
            new_lines = []
            x_line1 = None
            for i, line in enumerate(lines):
                if i == 0:
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    x_line1 = int(a * rho)
                    new_lines.append(line)
                else:
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    x_line = int(a * rho)
                    if x_line > x_line1+50:
                        new_lines.append(line)
                        break
            lines = new_lines

        for i,line in enumerate(lines):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            #print(f"lines: {len(lines)}  {rho}  {theta}")
            a = math.cos(theta)
            b = math.sin(theta)
            angle = -(np.degrees(theta)-90)
            if angle < 0:
                angle = 90 + (90 + angle)
            print(f"angle: {angle}")
            if angle > 45 and angle < 135:
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv.line(frame, pt1, pt2, (0,0,255), 3, cv.LINE_AA)   
                center = (int(x0),int(y0)+int(np.shape(frame)[0]/2))
                if i == 0:
                    line1 = (center, angle)
                elif i == 1:
                    line2 = (center, angle)
                #print(f"{(int(x0), int(y0)+int(np.shape(frame)[0]/2))}")
                cv.circle(frame,center,5,(255,255,255),4)
        if line1 != None and line2 != None:
                yaw = int((line1[1] + line2[1])/2) #target is 90°
                #pitch = 100 #constant slow
                roll = 0 
                throttle = 0

                if line2[0][0] > line1[0][0]:
                    roll = int(line1[0][0] + ((line2[0][0] - line1[0][0])/2))
                    throttle = (line2[0][0] - line1[0][0])

                else:
                    roll = int(line2[0][0] + ((line1[0][0] - line2[0][0])/2))
                    throttle = (line1[0][0] - line2[0][0])

                cv.circle(frame, (roll, 200), 5, (0,255,255),4)


        elif line1 != None:
            yaw = line1[1] #target is 90°


        print(f" throttle: {throttle}, roll: {roll}, pitch: constant, yaw: {yaw}")

    cv.imshow('lines',frame)
    return throttle, roll, 20, yaw



 
if __name__ == "__main__":
    cap = cv.VideoCapture("prueba1.mp4")
    #cap = cv.VideoCapture("prueba2.wmv")
    while True:
        if cap.isOpened():
            ret, frame = cap.read()
            frame = cv.resize(frame, (640,480))
            Start(frame)
            if cv.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                break
    cv.destroyAllWindows()
