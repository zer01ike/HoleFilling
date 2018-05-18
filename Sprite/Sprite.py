#-*- encoding=utf-8 -*-
import numpy as np
def singleton(cls,*args,**kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    return _singleton

@singleton
class Sprite(object):
    def setGS(self,c_median_min,DepthedImge,TexturedImage):
        height, width = DepthedImge.shape
        self.S = np.zeros((height, width, 3), np.uint8)
        self.G = np.zeros((height, width, 1), np.uint8)
        for i in range(0,height):
            for j in range(0,width):
                if DepthedImge[i,j] < c_median_min :
                    self.G[i][j] = DepthedImge[i,j]
                    for t in range(0,3):
                        self.S[i][j][t] = TexturedImage[i,j][t]
                else :
                    self.G[i][j] = 255
                    for t in range(0,3):
                        self.S[i][j][t] = 255

    def updateGS(self):
        pass
    def getG(self):
        return self.G
    def getS(self):
        return self.S
