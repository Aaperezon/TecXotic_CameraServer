import numpy as np
import cv2

def getColors(img, margin = 12):
    height, width,_ = np.shape(img)
    left_color_row,left_color_col = (int(height/2), int(margin))
    left_color = img[left_color_row,left_color_col]
    #print("Color izquierdo:"+str( left_color))
    image = cv2.circle(img, (left_color_col+30,left_color_row), 10, (int(left_color[0]),int(left_color[1]),int(left_color[2])), 2)
    image = cv2.circle(img, (left_color_col,left_color_row), 8, (0,0,0), 3)

    upper_color_row, upper_color_col = (int(margin),int(width/2)) 
    upper_color = img[upper_color_row,upper_color_col]
    #print("Color arriba:"+str( upper_color))
    image = cv2.circle(img, (upper_color_col,upper_color_row+30), 10,(int(upper_color[0]),int(upper_color[1]),int(upper_color[2])), 2)
    image = cv2.circle(img, (upper_color_col,upper_color_row), 8,(0,0,0), 3)

    right_color_row, right_color_col = (int(height/2),int(width-margin))
    right_color = img[right_color_row,right_color_col]
    #print("Color derecho:"+str( right_color))
    image = cv2.circle(img, (right_color_col-30,right_color_row), 10,(int(right_color[0]),int(right_color[1]),int(right_color[2])), 2)
    image = cv2.circle(img, (right_color_col,right_color_row), 8,(0,0,0), 3)
    return left_color,upper_color,right_color




def CompareColors(image1,image2):
    mov = { 0:(1,0,0), 1:(0,1,0)}
    low_limit_right = tuple(a - b for a, b in zip(tuple(image1[2]), (11,10,10)))  # HSV +- (2,20,30)
    up_limit_right = tuple(a + b for a, b in zip(tuple(image1[2]), (11,10,10)))
    for i in range(0, 2):
        if(tuple(image2[i]) >= low_limit_right and tuple(image2[i]) <= up_limit_right ):
            #print(f"Limite inferior: {low_limit_right}")
            #print(f"Limite superior: {up_limit_right}")
            return mov[i]


def Run():
    colors_img = []
    pictures = []
    large = (350,110)
    small = (125,110)
    for i in range(0,5):
        img = cv2.imread('./img'+str(i+1)+'.png')
        print("Tamano:" + str(np.shape(img)))
        width = np.shape(img)[1]
        height = np.shape(img)[0]
        if(width > (height*2)):
            width = large[0]
            height = large[1]
        else:
            width = small[0]
            height = small[1]
        img = cv2.resize(img,(width,height))
        #cv2_imshow(img)
        pictures.append(img)
        hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #cambiar la imagen de BGR a HSV
        #cv2_imshow(hsvFrame)
        color_img = getColors(hsvFrame)
        #print(color_img)
        colors_img.append(color_img)
        cv2.imshow("Color",hsvFrame)


    comparation_result = []
    for img1 in range(len(colors_img)):
        for img2 in range(len(colors_img)):
            if(np.array_equal(colors_img[img1],colors_img[img2]) == False):
                comparation = CompareColors(colors_img[img1],colors_img[img2])
                if(comparation != None):
                    print("La imagen"+str(img1+1)+"es igual a la imagen"+str( img2+1)+" por la" +str(comparation))
                    comparation_result.append( (img1, img2, comparation) )


    comparation_func = { (1,0,0):cv2.hconcat, (0,1,0):cv2.vconcat}

    comparation_relation = {}
    for count in range(len(comparation_result)):
        comp1 = comparation_result[count][0]
        comp2 = comparation_result[count][1]
        comparation_relation[comp1] = comp2
    #print(comparation_relation)


    aux = 0
    img_auxiliar = pictures[aux]
    finish_while = 0
    selected_picture = 0
    joker = None
    inserted_images = []
    while (finish_while < len(comparation_relation)-2 ):
        operation = comparation_result[selected_picture][2]
        if(operation != (0,1,0)):
            img2 = comparation_relation[aux]
            if(finish_while == 0):
                inserted_images.append(aux)
                inserted_images.append(img2)
            else:
                inserted_images.append(img2)
            img_auxiliar = comparation_func[operation]([img_auxiliar , pictures[img2]])
            aux = comparation_relation[aux]
            #cv2_imshow(img_auxiliar)
            finish_while = finish_while + 1
        else:
            selected_picture = selected_picture + 1
            aux = selected_picture
            img_auxiliar = pictures[aux]
            joker = finish_while
    print("La lista de insertados es:"+str( inserted_images))
    def Diff(li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    joker = Diff(range(len(pictures)), inserted_images)[0]
    print("Joker ="+str(joker))

    blank_space = { 0: (0,small[0]*2+large[0]), 1: (small[0], small[0]+large[0]), 2:(small[0]+large[0],small[0]), 3:(small[0]*2+large[0],0)    }
    for index in range(len(inserted_images)):
        size_temp = np.shape(pictures[inserted_images[index]])
        if(size_temp[1] == large[0] and np.array_equal(colors_img[inserted_images[index]][1],colors_img[joker][1] ) == False ):
            #print("Caso Blank_space:"+str(index))
            blank = np.zeros([small[1], blank_space[index][0],3],dtype=np.uint8)
            blank.fill(255)
            #print("Tamano Blank "+str(np.shape(blank)) + "  "+str(np.shape(pictures[joker])))
            joker1  = cv2.hconcat([blank, pictures[joker]])
            #print("Tamano blank vs picture joekr"+str(np.shape(blank))+"  " + str(np.shape(pictures[joker])))
            blank = np.zeros([small[1], blank_space[index][1],3],dtype=np.uint8)
            blank.fill(255)
            joker1  = cv2.hconcat([joker1, blank])
            #print("Tamano joker vs img_auxiliar"+str( np.shape(joker1)) +"  "+str(np.shape(img_auxiliar)))

            joker1  = cv2.vconcat([joker1, img_auxiliar])

            #cv2.imshow(joker1)
            return joker1

            #print(f"Aqui iria la imagen arriba1 {index}") 

#Run(img1,img2)
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    pic_counter = 1
    pic_shot = True
    pic_on = False
    cambiar_grid = False
    while True:
        ret, frame = cap.read()
        large = (350,110)
        small = (125,110)
        #640 x 480
        start_point = (150,150)
        end_point = None
        if(cv2.waitKey(1) & 0xFF == ord('d')):
            cambiar_grid = not cambiar_grid
        if(cambiar_grid == True):
            end_point = tuple(a + b for a, b in zip(start_point, large))
        else:
            end_point = tuple(a + b for a, b in zip(start_point, small))
        
        cv2.rectangle(frame, start_point, end_point, (0,255,0), 1)

        
        
        if(cv2.waitKey(1) & 0xFF == ord('a')):
            pic_on = True
        else:
            pic_shot = True
            pic_on = False

        if(pic_on == True and pic_shot == True):
            startRow = int(start_point[1])
            startCol = int(start_point[0])
            endRow = int(end_point[1])
            endCol = int(end_point[0])
            frame = frame[ startRow:endRow, startCol:endCol ]
            cv2.imwrite('./img'+str(pic_counter)+'.png', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])
            pic_counter = pic_counter + 1
            print("Foto creada")
            pic_shot = False


      



        """
        frame = Run()
        print(frame)
        """
        cv2.imshow("video",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


