import cv2
import numpy as np
import subprocess



cap=cv2.VideoCapture(0)

while True:
    _,gray=cap.read()
    #gray=cv2.pyrMeanShiftFiltering(gray,10,30)
    gray=cv2.blur(gray,ksize=(5,5))
    gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
    gray=cv2.resize(gray,(300,200))
    Sobel=cv2.Sobel(gray,ddepth=cv2.CV_8U,ksize=1,dx=1,dy=0)
    ret,threshold=cv2.threshold(Sobel,0,255,(cv2.THRESH_OTSU+cv2.THRESH_BINARY))
    k=cv2.getStructuringElement(cv2.MORPH_RECT,ksize=(30,55))
    threshold=cv2.morphologyEx(threshold,cv2.MORPH_CLOSE,k)
    contours,hierarchy=cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    rect=cv2.minAreaRect(contours[0])
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    threshold=cv2.drawContours(gray,[box],-1,(0,255,255),1)

    height,width=threshold.shape[:]

    mask1=np.zeros((height+2,width+2),np.uint8)
    cv2.floodFill(threshold,mask1,(0,0),255,flags=cv2.FLOODFILL_MASK_ONLY)
    mask_inv=cv2.bitwise_not(threshold)

    mask=np.zeros(threshold.shape[:-1],dtype="uint8")
    screenCnt=None
    for c in contours:
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.02*peri,True)
        x,y,w,h=cv2.boundingRect(c)
        print(cv2.contourArea(c))
        cv2.rectangle(gray,(x,y),(x+w,y+h),(0,0,255),3)
        roi=gray[y:y+h,x:x+w]
        if len(approx)==4:
            screenCnt=approx
            break





    cv2.imshow('roi',roi)
    cv2.imshow('frame',gray)
    cv2.imshow('sobel',Sobel)
    cv2.imshow('threshold',threshold)

    if    cv2.waitKey(1) & 0xFF==ord('s'):
        cv2.imwrite('op.jpg',roi)





    elif cv2.waitKey(1)  & 0xFF==ord('q'):
        break

    print(subprocess.call('tesseract.exe --dpi 300 op.jpg bla.txt',shell=True))
    f=open('bla.txt.txt','r')
    message=f.read()
    print(message)
    f.close()
cap.release()
cv2.destroyAllWindows()





