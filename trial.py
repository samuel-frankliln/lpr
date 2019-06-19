import cv2
import numpy as np
import math
import argparse
import subprocess

gray= cv2.imread(r'C:\Users\Samuel\PycharmProjects\license_plate_recognition\images.jpg' )
gray=cv2.pyrMeanShiftFiltering(gray,10,30)
gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
img=cv2.imread(r'C:\Users\Samuel\PycharmProjects\license_plate_recognition\images.jpg')
img=cv2.resize(img,(300,200))
gray=cv2.resize(gray,(300,200),interpolation=cv2.INTER_AREA)
cv2.imshow('og',gray)


gray=cv2.blur(gray,ksize=(5, 5))

Sobel=cv2.Sobel(gray,ddepth=cv2.CV_8U,ksize=1,dx=1,dy=0)

ret,threshold=cv2.threshold(Sobel,0,255,(cv2.THRESH_BINARY+cv2.THRESH_OTSU))

k=cv2.getStructuringElement(cv2.MORPH_RECT,ksize=(30,55),)

threshold=cv2.morphologyEx(threshold,cv2.MORPH_CLOSE,k)

contours, hierarchy=cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

#threshold=cv2.drawContours(threshold,contours,-1,(0,255,255),10)

rect = cv2.minAreaRect(contours[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
threshold=cv2.drawContours(img,[box],-1,(0,255,255),1)
#not sure what have i done here just took 0th element and luckily is the license plate ,have to constraintsts like aspect ration(52%)  book opencv

print(len(contours))

print(contours[0])

height, width = threshold.shape[:-1]


mask1 = np.zeros((height+2, width+2), np.uint8)     # line 26
cv2.floodFill(threshold,mask1,(0,0),255,flags=cv2.FLOODFILL_MASK_ONLY)     # line 27
mask_inv=cv2.bitwise_not(threshold)

mask = np.zeros(threshold.shape[:2], dtype="uint8")
screenCnt = None
for c in contours:
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*peri,True)
    x,y,w,h = cv2.boundingRect(c)
    print (cv2.contourArea(c))
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
    roi = img[y:y+h, x:x+w]
    if len (approx)==4:
        screenCnt = approx
        break


print(len(contours))
cv2.imshow('img',threshold)
cv2.imshow('new',mask_inv)
cv2.imshow('roi',roi)
#cv2.imshow('plate',crop)
k=cv2.waitKey(0) & 0xFF

print(subprocess.call('tesseract.exe op.jpg bla.txt',shell=True))

f=open('bla.txt.txt','r')
message=f.read()
print(message)
f.close()

#print(os.system(tesseract.exe,op.jpg ))
if k==27:
    cv2.destroyAllWindows()
elif k==ord('s'):
    cv2.imwrite('op.jpg',roi)


cv2.waitKey(0)
cv2.destroyAllWindows()

