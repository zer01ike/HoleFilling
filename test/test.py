import cv2
import numpy as np
from InitialHoleFilling import initial
TexturedImg = cv2.imread('../DataSet/Sequence/Warped/text_0_w.bmp',1)
TexturedImg2 = cv2.imread('initial_fill.bmp',1)
# px = TexturedImg[2,2]
# hole = np.array([175,188,184])
# if (px == hole).all() :
#     print ('yes')
# print(px)

# a = initial.Initial()
# hole = np.array([200,200,200])
# a.laplacian(TexturedImg,hole)
# cv2.imshow("fill",TexturedImg)
# cv2.imwrite("initial_fill.bmp",TexturedImg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
print(TexturedImg[128,82])
print(TexturedImg[128, 81][0])
for i in range(0,3):
    print(int((int(TexturedImg[128, 81][i]) + int(TexturedImg[128, 83][i]) + int(TexturedImg[127, 82][i]) +
               int(TexturedImg[129, 82][i])) / 4))
print(TexturedImg2[128,82])