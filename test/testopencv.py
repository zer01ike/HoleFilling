import cv2
import sys
sys.path.append("..")
from Warping import Warping
# img =  cv2.imread("test.jpg", 0)
# px = img[2,2]
# print(px)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows( )

depthedimg = cv2.imread('depth00300.jpg',0)
TexturedImg = cv2.imread('image00300.jpg',1)

W1d = Warping.warping()
output_image = W1d.warpingwith1D(TexturedImg, depthedimg)
cv2.imshow('image',output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()