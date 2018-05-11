from DepthFilling import DepthFilling
import cv2

DepthedImg = cv2.imread('ballons_d_warping_0.jpg', 0)

DF = DepthFilling.DepthFilling(DepthedImg,63,63)
#depth_filled =  DF.testKmeans(DepthedImg)
depth_filled  = DF.depthfill()
cv2.imshow('depth', depth_filled)
cv2.imwrite('depth63_0_ballons.jpg',depth_filled)
cv2.waitKey(0)
cv2.destroyAllWindows()
