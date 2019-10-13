import numpy as np
import cv2
import pyautogui
pyautogui.FAILSAFE = False
import math


def calculateAngle(far, start, end):
    """Cosine rule"""
    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
    angle = math.acos((b**2 + c**2 - a**2) / (2*b*c))
    return angle

#This one is going to be of use....
def countFingers(contour):
    hull = cv2.convexHull(contour, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(contour, hull)
        cnt = 0
        if type(defects) != type(None):
            for i in range(defects.shape[0]):
                #Calculating the angle form the defects
                s, e, f, d = defects[i, 0]
                start = tuple(contour[s, 0])
                end = tuple(contour[e, 0])
                far = tuple(contour[f, 0])
                angle = calculateAngle(far, start, end)
                # Ignore the defects which are small and wide
                # Probably not fingers
                if d > 10000 and angle <= math.pi/2:
                    cnt += 1
        return (True, cnt)
    return (False, 0)
    
    
cap = cv2.VideoCapture(0)

while True:
    #Recording the video
    _,frame = cap.read()
    #Resize the mask to the size of your screen
    frame = cv2.flip(cv2.resize(frame,(1366,768)),1)
    #Making the hsv image
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #The color range for that blue glove.....
    lower_red = np.array([100,50,20])
    upper_red = np.array([150,255,255])
    #Generating the mask
    mask = cv2.inRange(hsv,lower_red,upper_red)
    #Some erossion and dialation
    mask = cv2.erode(mask,None,iterations=2)

    #Lets find the contour for the mask
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
                c = max(contours,key=cv2.contourArea)
                if cv2.contourArea(c)>1000:
                    #Getting the bounding rectangle
                    x,y,w,h = cv2.boundingRect(c)
                    #Drawing the bounding rectangle
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    #Getting the moments
                    m = cv2.moments(c)
                    #moving mouse to the centroid
                    pyautogui.moveTo(x+w,y)
                    count = countFingers(c)
                    #########Add the clicking logic here


    #Lets see what we have got here
    #cv2.imshow("Video",frame)
    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break
    #Press q to exit from camera
    
cap.release()  #Release the camera (necessary)
cv2.destroyAllWindows()
