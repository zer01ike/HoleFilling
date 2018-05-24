from DepthFilling import DepthFilling
import cv2

DepthedImg = cv2.imread('../DataSet/Sequence/Warped/depth_0_w.bmp', 0)

DF = DepthFilling.DepthFilling(DepthedImg,63,63)
#depth_filled =  DF.testKmeans(DepthedImg)
depth_filled  = DF.depthfill()
cv2.imshow('depth', depth_filled)
cv2.imwrite('depthfill_book_0.bmp',depth_filled)
cv2.waitKey(0)
cv2.destroyAllWindows()
