import numpy as np
import cv2
import math

class TextureRefine():
    def __init__(self,TextureImage,IniatialImage,DepthImage,HoleList):
        self.TextureImage = cv2.imread(TextureImage)
        self.InitialImage = cv2.imread(IniatialImage)
        self.DepthImage = cv2.imread(DepthImage,0)
        self.HoleList = HoleList
        self.height,self.width,self.channels= self.TextureImage.shape

    def setGradientMap(self):

        sobelx = cv2.Sobel(cv2.cvtColor(self.TextureImage,cv2.COLOR_RGB2GRAY),cv2.CV_64F,1,0,ksize=-1)
        sobely = cv2.Sobel(cv2.cvtColor(self.TextureImage,cv2.COLOR_RGB2GRAY),cv2.CV_64F,0,1,ksize=-1)
        sobelx_2 = 0
        sobely_2 = 0

        sobelx = cv2.pow(sobelx,2)
        sobely = cv2.pow(sobely,2)

        sum = np.add(sobelx,sobely)
        self.TextureGradientMap = np.sqrt(sum)
        #print(self.TextureGradientMap)

        sobelx = cv2.Sobel(cv2.cvtColor(self.InitialImage,cv2.COLOR_RGB2GRAY), cv2.CV_64F, 1, 0, ksize=-1)
        sobely = cv2.Sobel(cv2.cvtColor(self.InitialImage,cv2.COLOR_RGB2GRAY), cv2.CV_64F, 0, 1, ksize=-1)
        sum = cv2.pow(sobelx, 2) + cv2.pow(sobely, 2)
        self.InitialGradientMap = np.sqrt(sum)


    def LossFunction(self,patchsize,c_i,c_j,x_i,x_j):
        #c_center comes from the HoleList
        #x_center comes from the the 5* patchsize around the c_center

        #k = pathcsize * patchsize
        #Ko = intialed number
        x = self.get_kernel_content(x_i, x_j,patchsize,self.TextureImage)
        c = self.get_kernel_content(c_i, c_j,patchsize,self.TextureImage)

        x_initial = self.get_kernel_content(x_i,x_j,patchsize,self.InitialImage)
        c_initial = self.get_kernel_content(c_i,c_j,patchsize,self.InitialImage)

        gx = self.get_gradient_content(x_i,x_j,patchsize,self.TextureGradientMap)
        gc = self.get_gradient_content(c_i,c_j,patchsize,self.TextureGradientMap)

        gx_initial = self.get_gradient_content(x_i,x_j,patchsize,self.InitialGradientMap)
        gc_initial = self.get_gradient_content(c_i,c_j,patchsize,self.InitialGradientMap)
        #part 1

        E = 0
        P1 = 0
        for i in range(0,patchsize*patchsize):
             P1 +=  np.square(x[i]-c[i])
        #part 2
        P2 = 0
        for i in range(0,patchsize*patchsize):
            # if it's initial
            P2 += np.square(x_initial[i] - c_initial[i])
            pass
        #part 3
        P3 = 0
        for i in range(0,patchsize*patchsize):
            P3 += np.square(gx[i] - gc[i])

        P4 = 0
        for i in range(0,patchsize*patchsize):
            P4 += np.square(gx_initial[i] - gc_initial[i])

        E = P1+0.6*P2 +0.6*P3+0.6*0.6*P4

        return E

    def findPatchLoc(self, stepsize, x,y):
        E_List = []

        # get the region of X
        for x_s in range ((0 if int(x-2.5*stepsize)<0 else int(x-2.5*stepsize)) , (self.height if int(x+2.5*stepsize)>self.height else int(x+2.5*stepsize))):
            for y_s in range((0 if int(y-2.5*stepsize)<0 else int(y-2.5*stepsize)),(self.width if int(y+2.5*stepsize)>self.width else int(y+2.5*stepsize))):
                if x_s ==x and y_s == y :continue
                if self.DepthImage[x_s,y_s] >= self.DepthImage[x,y]+15 : continue
                if [x_s,y_s] in self.HoleList : continue
                E_temp = self.LossFunction(stepsize,x,y,x_s,y_s)
                E_List.append([E_temp,x_s,y_s])

        #E_List arrange
        first_ele = lambda s:s[0]

        list = sorted(E_List, key = first_ele)

        return list[0]

    def updateImage(self,stepsize):
        self.setGradientMap()
        total = len(self.HoleList)
        index =0
        #######################test
        # x, y = self.HoleList[13050]
        #
        # loc = self.findPatchLoc(stepsize,x,y)
        # x_i = loc[1]
        # x_j = loc[2]
        # #     #using (x_i,x_j) to replace (x,y)
        # self.replace(stepsize,x,y,x_i,x_j)
        # index +=1
        # print(str(index)+'/'+str(x)+','+str(y)+'/'+str(total)+"::processed!")
        # for i in range(0,3):
        #     self.InitialImage[x,y][i] = 100
        #     self.InitialImage[x_i,x_j][i] = 100
        # print(str(x_i)+" "+str(x_j))

        ########################

        for i in self.HoleList:
            x,y = i
            loc = self.findPatchLoc(stepsize,x,y)
            if len(loc) == 0 :
                x_i = x
                x_j = y
            else :
                x_i = loc[1]
                x_j = loc[2]
            #using (x_i,x_j) to replace (x,y)
            self.replace(stepsize,x,y,x_i,x_j)
            index +=1
            print(str(index)+'/'+str(i)+'/'+str(total)+"::processed!")
        return self.InitialImage

    def replace(self,stepsize,x,y,x_i,y_j):
        for i in range(0,int(stepsize/2)+1):
            for j in range(0,int(stepsize/2)+1):
                if x-i < 0 or x_i -i< 0 : continue
                if y-j < 0 or y_j - j<0: continue
                if x+i >=self.height or x_i +i >=self.height: continue
                if y+j >=self.width or y_j + j >=self.width: continue
                self.InitialImage[x - i, y - j] = self.InitialImage[x_i - i, y_j - j]
                self.InitialImage[x - i, y + j] = self.InitialImage[x_i - i, y_j + j]
                self.InitialImage[x + i, y + j] = self.InitialImage[x_i + i, y_j + j]
                self.InitialImage[x + i, y - j] = self.InitialImage[x_i + i, y_j - j]


    def get_kernel_content(self,i,j,kernel_size,Image):
        kernel_content = np.zeros(kernel_size * kernel_size)
        half = int(kernel_size / 2)
        index = 0
        for kernel_v in range((0 if i - half <0 else i-half), (self.height if i + half + 1>self.height else i+half+1)):
            for kernel_h in range((0 if j - half<0 else j-half), (self.width if j + half + 1>self.width else j+half+1)):
                kernel_content[index] = self.getluminance(kernel_v,kernel_h,Image)
                index += 1
        return kernel_content

    def get_gradient_content(self,i,j,kernel_size,Image):
        gradient_content = np.zeros(kernel_size * kernel_size)
        half = int(kernel_size / 2)
        index = 0
        for kernel_v in range((0 if i - half <0 else i-half), (self.height if i + half + 1>self.height else i+half+1)):
            for kernel_h in range((0 if j - half<0 else j-half), (self.width if j + half + 1>self.width else j+half+1)):
                gradient_content[index] = Image[kernel_v][kernel_h]
                index += 1
        return gradient_content

    def getluminance(self,i,j,Image):

        if i<0 :return 0
        if j<0 :return 0
        if i>=self.height :return 0
        if j>=self.width : return 0

        return 0.1*Image[i,j][0] + 0.6 * Image[i,j][1] + 0.3 * Image[i,j][2]