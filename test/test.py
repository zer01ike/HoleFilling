import cv2
import numpy as np
from InitialHoleFilling import initial
TexturedImg = cv2.imread('../DataSet/Sequence/Warped/text_0_w.bmp', 1)
height,width,channel = TexturedImg.shape
#first-round hollfilling with the background pixels
virtual_image = np.zeros((height, width, 3), np.uint8)
print(TexturedImg.shape)
t=0
print(TexturedImg[0,0][0:3])

def depthfillA1_2():
    for i in range(0,height):
        for j in range(0,width):
            if TexturedImg[i,j][0]== 255 and TexturedImg[i,j][1] == 255 and TexturedImg[i,j][2] == 255:
                virtual_image[i][j][0] = 255
                virtual_image[i][j][1] = 255
                virtual_image[i][j][2] = 255

    for i in range(0,height):
        for j in range(0,width):
            if j>3 and TexturedImg[i,j][0]== 255 and TexturedImg[i,j][1] == 255 and TexturedImg[i,j][2] == 255:
                TexturedImg[i,j][0] = TexturedImg[i,j-3][0]
                TexturedImg[i, j][1] = TexturedImg[i, j - 3][1]
                TexturedImg[i, j][2] = TexturedImg[i, j - 3][2]



    Mask = cv2.imread('../DataSet/Sequence/Warped/text_0_w.bmp', 0)
    dst = cv2.inpaint(TexturedImg, Mask, 3, cv2.INPAINT_TELEA)
    cv2.imshow("test",TexturedImg)
    cv2.imshow('virtual',virtual_image)
    cv2.imshow('inpaint',dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#TexturedImg2 = cv2.imread('initial_fill.bmp',1)
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
# print(TexturedImg[128,82])
# print(TexturedImg[128, 81][0])
# for i in range(0,3):
#     print(int((int(TexturedImg[128, 81][i]) + int(TexturedImg[128, 83][i]) + int(TexturedImg[127, 82][i]) +
#                int(TexturedImg[129, 82][i])) / 4))
# print(TexturedImg2[128,82])
