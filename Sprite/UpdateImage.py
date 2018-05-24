import cv2
class updateImage():
    def __init__(self,TextureImage,DepthImage,DepthSprite,TextureSprite,B,HoleList):
        self.TextureImage = cv2.imread(TextureImage)
        self.DepthImage = cv2.imread(DepthImage)
        self.DepthSprite = cv2.imread(DepthSprite)
        self.TextureSprite = cv2.imread(TextureSprite)
        self.B = B
        self.HoleList = HoleList

    def update(self):
        #TextureImage and DepthSprite and TextureSprite are all cv2.read object
        height,width,channels = self.TextureImage.shape()

        # loc is in the hole area not the every location
        #for i in range(0,height):
            #for j in range(0,width):
                #self.TextureImage[i,j] = self.TextureSprite[i,j] if self.DepthImage[i,j] < self.DepthSprite[i,j] +B else 0

        for i in range(0,self.HoleList.size):
            x, y = self.HoleList[i]
            self.TextureImage[x, y] = self.TextureSprite[x, y] if self.DepthImage[x, y] < self.DepthSprite[x, y] + self.B else 0

    def getTextureImage(self):
        return self.TextureImage


