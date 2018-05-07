from DepthFilling import DepthFilling
import cv2

DepthedImg = cv2.imread('distation_depth00300.jpg', 0)

DF = DepthFilling.DepthFilling()
depth_filled =  DF.testKmeans(DepthedImg)
#depth_filled  = DF.DepthFill(DepthedImg,32)
cv2.imshow('depth', depth_filled)
cv2.imwrite('depth32_new.jpg',depth_filled)
cv2.waitKey(0)
cv2.destroyAllWindows()
