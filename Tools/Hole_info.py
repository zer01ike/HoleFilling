import cv2
import numpy as np
class Hole():
    def __init__(self,Image,HoleValue):
        self.Image = cv2.imread(Image)
        self.LocList = []
        self.HoleValue = HoleValue

    # return if this location is the center of the patch
    def isCenter(self, Loc, length):
        pass
    def getLoc(self):
        return self.LocList

    def findLoc(self):
        height, width, channel = self.Image.shape
        for i in range(0,height):
            for j in range(0, width):
                if (self.Image[i, j] == self.HoleValue).all():
                    self.LocList.append([i, j])


