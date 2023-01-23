import cv2
import cvzone
import numpy as np
import pickle
width , height = (158 - 50), (240-192)

cap = cv2.VideoCapture('carPark.mp4')
with open('CarParkPos', 'rb') as f:
    poslist = pickle.load(f)

def checkparkingspace(imgPro):
    spaceCounter = 0
    for pos in poslist:

        x,y = pos
        # cv2.rectangle(img,pos,(pos[0]+width , pos[1]+height), (255, 0, 255), 2)
        cv2.imshow('car' , img)

        imgcrop = imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x+y) , imgcrop)
        count = cv2.countNonZero(imgcrop)
        cvzone.putTextRect(img,str(count),(x,y+height-2),scale=1,thickness=2,offset=0,colorR=(0,0,255))
        if count < 500:
            color = (0,255,0)
            thickness = 5
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img, f'Free{str(spaceCounter)}/{len(poslist)}', (450,50), scale=2, thickness=2, offset=10, colorR=(0, 255,0))



while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    sucess, img = cap.read()


    imgGray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray , (3,3) , 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.zeros((3,3) , np.uint8)
    imgdilate = cv2.dilate(imgMedian , kernel , iterations = 1)


    checkparkingspace(imgdilate)
    # for pos in poslist:
    #     x,y = pos

    
    cv2.imshow('car', img)
    # cv2.imshow('blur', imgBlur)
    # cv2.imshow('thres', imgThreshold)
    # cv2.imshow('median', imgMedian)
    # cv2.imshow('dilate', imgdilate)
    cv2.waitKey(1)


