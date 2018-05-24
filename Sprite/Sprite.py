#-*- encoding=utf-8 -*-
import numpy as np
class Sprite(object):
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.S = np.zeros((self.height, self.width, 3), np.uint8)
        self.G = np.zeros((self.height, self.width, 1), np.uint8)
        for i in range(0 ,self.height):
            for j in range(0, self.width):
                for t in range(0,3):
                    self.S[i][j][t] = 255
                self.G[i][j] = 255

    def setGS(self,c_median_min,DepthedImage,TexturedImage):
        for i in range(0,self.height):
            for j in range(0,self.width):
                if DepthedImage[i,j] < c_median_min :
                    self.G[i][j] = DepthedImage[i,j]
                    for t in range(0,3):
                        self.S[i][j][t] = TexturedImage[i,j][t]
                #else :
                    #self.G[i][j] = 255
                    #for t in range(0,3):
                        #self.S[i][j][t] = 255

    def updateGS(self):
        pass
    def getG(self):
        return self.G
    def getS(self):
        return self.S
