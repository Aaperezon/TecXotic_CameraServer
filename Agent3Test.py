import cv2 as cv


picture = [0]
def Start(frame, action):
    global picture
    if(cv.waitKey(1) & action == True):
        picture = frame

    frame = cv.resize(frame, (320,240))
    cv.imshow("video", frame)
    if any(picture):
        picture = cv.resize(picture, (320,240))
        cv.imshow("picture", picture)

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    while True:
        _, frame = cap.read()
        if cv.waitKey(1) & 0xFF == ord('d'):
            Start(frame, True)
        else:
            Start(frame, False)
            
            
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv.destroyAllWindows()


