import cv2
import numpy as np

TexturedImg = cv2.imread('test.jpg',1)
height,width,channle = TexturedImg.shape
slice_window = TexturedImg[::,::9,::9]
print(slice_window[0])
for i in range(0,len(slice_window)):
    cv2.imshow('test'+str(i),slice_window[i])

cv2.waitKey(0)
cv2.destroyAllWindows()