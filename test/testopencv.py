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

DepthedImg = cv2.imread('../DataSet/testSequence_depth/0.jpg', 0)
TexturedImg = cv2.imread('../DataSet/testSequence/0.jpg', 1)
cv2.imshow('orginal_text',TexturedImg)

W1d = Warping.warping()
output_txt_image, output_depth_image = W1d.warpingwith1D(TexturedImg, DepthedImg)
cv2.imshow('image', output_txt_image)
cv2.imshow('depth', output_depth_image)
cv2.imwrite('ballons_d_warping_0.jpg',output_depth_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
