import cv2
import numpy as np

video = cv2.VideoCapture(0)
video.set(3,648)
video.set(4,480)
video.set(10,150)

mycolors = [[0,84,113,8,231,255],
            [19,68,255,34,235,255],
            [85,55,72,114,255,178],
            [104,105,140,115,208,255]]

color_values = [[0,0,255],       #BGR
                [0,255,255],
                [0,255,0],
                [255,0,0]]

mypoints = []   #format-[x,y,colorid in mycolors]

def find_colour(img,mycolors,color_values):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    count=0
    new_points=[]
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imageHSV, lower, upper)
        x,y=getcontours(mask)
        cv2.circle(imagecopy,(x,y),10,color_values[count],cv2.FILLED)
        if x!=0 and y!=0:
            new_points.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return new_points

def getcontours(img):
    contour,hierarchy=cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    x,y,width,height=0,0,0,0
    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area>500:
            perimeter = cv2.arcLength(cnt, True)
            approx=cv2.approxPolyDP(cnt,0.02*perimeter,True)
            #cv2.drawContours(imagecopy, cnt, -1, (255, 0, 0), 2)
            x,y,width,height=cv2.boundingRect(approx)
    return (x+width//2),y

def draw_points(mypoints,mycolors):
    for points in mypoints:
        cv2.circle(imagecopy, (points[0],points[1]), 5, mycolors[points[2]], cv2.FILLED)

while True:
    succ, image = video.read()
    imagecopy = image.copy()
    new_points = find_colour(image,mycolors,color_values)
    if len(new_points)!=0:
        for newp in new_points:
            mypoints.append(newp)
    if len(mypoints)!=0:
        draw_points(mypoints,color_values)
    cv2.imshow("web", imagecopy)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break