import numpy as np
import cv2
import math

def GetLines(contour, idLinea):
  #global img
  lenContour = len(contour)
  if(lenContour >= 2 and idLinea < lenContour):
    rotrect = cv2.minAreaRect(contour[idLinea])
    box = cv2.boxPoints(rotrect)
    box = np.int0(box)
    x1 = box[0][0]
    y1 = box[0][1]
    x2 = box[2][0]
    y2 = box[2][1]
    #print((x1,y1), (x2,y2))
    #print(box)
    #cv2.drawContours(img,[box],0,(0,255,0),2)
    angulo = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if(angulo <= -1):
      angulo = 90 - (90+(angulo))
    else:
      angulo = 90 + (90-(angulo))
    giro = (90-angulo)
    magnitud = int(math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2)))
    return ((x1,y1), (x2,y2) , angulo, giro, magnitud)
  else:
    return ((0,0), (0,0) , 0, 0, 0)

def Run(img):
  #img = cv2.resize(img, (640, 480)) 

  hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #cambiar la imagen de BGR a HSV
  img = cv2.medianBlur(img,7)   #elimina el ruido opacando la imagen
  blue_low = np.array([88, 100, 90], np.uint8)
  blue_high = np.array([130, 255, 255], np.uint8)
  blue_mask = cv2.inRange(hsvFrame, blue_low, blue_high)  #crea la mascara para el color azul
  cv2.imshow("Blue Mask",blue_mask)

  contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  contour = np.array(sorted(contours, key=len, reverse=True))

  L1P1, L1P2 , angulo1, giro1, magnitud1 = GetLines(contour, 0)
  L2P1, L2P2 , angulo2, giro2, magnitud2 = GetLines(contour, 1)
  print("Line 1:"+str(L1P1)+" "+str(L1P2))
  print("Line 1:"+str(L2P1)+" "+str(L2P2))
  angulo = int((angulo1+angulo2)/2)
  giro = int((giro1+giro2)/2)
  print("Angulo: "+str(angulo))
  print("Giro: "+str(giro))
  cv2.line(img, L1P1,L1P2, (0,255,0), 3, cv2.LINE_AA)
  cv2.line(img, L2P1,L2P2, (0,255,0), 3, cv2.LINE_AA)

  print("Magnitud Linea 1: "+str(magnitud1))
  print("Magnitud Linea 2: "+str(magnitud2))
  distancia = int(math.sqrt(math.pow(L2P2[0]-L2P1[0],2)+math.pow(L1P2[1]-L1P1[1],2)))
  print("Distancia:"+ str(distancia))

  height,width = img.shape[:2]
  print("width :"+ str(width)+"height : " +str(height))

  centro = width/2
  if(L1P1[0] > L2P1[0]): #Significa que L1P1 = linea de la izquierda
    if(L1P1[0] > int(centro+(centro*.2)) and L2P1[0] < int(centro-(centro*.2))):
      print("Muevete a la RECTO")
    elif(L1P1[0] < int(centro+(centro*.2)) and L2P1[0] < int(centro-(centro*.2)) ):
      print("Muevete a la DERECHA")
    elif(L1P1[0] > int(centro+(centro*.2)) and L2P1[0] > int(centro-(centro*.2)) ):
      print("Muevete a la IZQUIERDA")
  elif (L2P1[0] > L1P1[0]): #Significa que L2P1 = linea de la derecha
    if(L2P1[0] > int(centro+(centro*.2)) and L1P1[0] < int(centro-(centro*.2))):
      print("Muevete a la RECTO")
    elif(L2P1[0] < int(centro+(centro*.2)) and L1P1[0] < int(centro-(centro*.2)) ):
      print("Muevete a la DERECHA")
    elif(L2P1[0] > int(centro+(centro*.2)) and L1P1[0] > int(centro-(centro*.2)) ):
      print("Muevete a la IZQUIERDA")
  cv2.imshow("Result",img)

if __name__ == "__main__":
  cap = cv2.VideoCapture(0)
  while True:
    ret, frame = cap.read()
    Run(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  cap.release()
  cv2.destroyAllWindows()