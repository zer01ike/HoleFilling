from Tools import Hole_info
import cv2
import numpy as np
hole = np.array([255,255,255])
holeLoc = Hole_info.Hole("../DataSet/Sequence/Warped/texture/0.bmp",hole)
holeLoc.findLoc()
c=holeLoc.getLoc()
x,y = c[0]
print(x,y)