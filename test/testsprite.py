from DepthFilling import DepthFilling
from Sprite import Sprite
import numpy as np
import cv2

DepthedImg = cv2.imread('../main/Sequence/Warped/depth_0_w.bmp', 0)
TexturedImg = cv2.imread('../main/Sequence/Warped/text_0_w.bmp',1)

# DF = DepthFilling.DepthFilling(DepthedImg,63,63)
# #depth_filled =  DF.testKmeans(DepthedImg)
# depth_filled  = DF.depthfill()
# print(DF.get_median_cmin())

cmin_median = 88.523132718
currentSprite = Sprite.Sprite()

currentSprite.setGS(cmin_median,DepthedImg,TexturedImg)

cv2.imwrite('testSpriteDepth.bmp',currentSprite.getG())
cv2.imwrite('testSpriteTexture.bmp',currentSprite.getS())