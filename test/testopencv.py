import cv2
import sys

sys.path.append("..")
from Warping import Warping
#
# img =  cv2.imread("test.jpg", 1)
# px = img[2,2]
# print(px)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows( )

DepthedImg = cv2.imread('../main/Sequence/Original/depth1.bmp', 0)
TexturedImg = cv2.imread('../main/Sequence/Original/text1.bmp', 1)
cv2.imshow('orginal_text',TexturedImg)

W1d = Warping.warping()
output_txt_image, output_depth_image = W1d.warpingwith1D(TexturedImg, DepthedImg)
cv2.imshow('image', output_txt_image)
cv2.imshow('depth', output_depth_image)
cv2.imwrite('../main/Sequence/Warped/depth_1_w.bmp',output_depth_image)
cv2.imwrite('../main/Sequence/Warped/text_1_w.bmp',output_txt_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
