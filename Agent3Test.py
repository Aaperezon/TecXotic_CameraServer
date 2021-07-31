import cv2 as cv
import os

picture = [0]
picture_index = 0
picture_name = "./Agent3_img/agent3_"
picture_extension = ".png"


def OrganizePictures():
    if picture_index == 6:
        image = []
        for i in range(5):
            image.append(cv.imread(picture_name+str(i)+picture_extension))
            

def Start(frame, shoot, delete):
    global picture, picture_index
    if shoot == False and delete == False:
        return
    if shoot == True:
        picture = frame
    if delete == True:
        picture_index -= 1
        os.remove(picture_name+str(picture_index)+picture_extension)
        print(f"deleted: {picture_name+str(picture_index)+picture_extension}")

    if  len(picture) > 1:
        picture = cv.resize(picture, (320,240))
        cv.imshow("picture", picture)
        cv.imwrite(picture_name+str(picture_index)+picture_extension,picture)
        print(f"creating: {picture_name+str(picture_index)+picture_extension}")
        picture = [0]
        picture_index += 1

if __name__ == "__main__":
    cap = cv.VideoCapture(2)
    while True:
        _, frame = cap.read()
        frame = cv.resize(frame, (320,240))
        
        if cv.waitKey(1) & 0xFF == ord('s'):
            Start(frame, True, False)
        elif cv.waitKey(1) & 0xFF == ord('d'): 
            Start(frame, False, True)
        else:
            Start(frame, False, False)
            
        cv.imshow("video", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv.destroyAllWindows()


