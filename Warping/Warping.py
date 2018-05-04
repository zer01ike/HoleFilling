import numpy as np
class warping():
    def warpingwith1D(self,TexturedImage,DepthedImage):
        table = []
        knear = 0  #the near is 0
        kfar = 128 #the far is 128
        eye_seperation = 6 #means the seperation of the two eye is the 6cm
        view_distance = 800 # the view distance is 3m
        Npix = 320 #standard definition display to reduce the pararllex
        S = 25 # depth = 0, maxium shift .
        height,width,channels = TexturedImage.shape
        print(width,height,channels)
        #print(DepthedImage[700,575])
        warping_image = np.zeros((height,width,3),np.uint8)
        print (warping_image[500][500])
        for i in range(0,256):
            A = i *(knear/64 + kfar/16)/255
            h = -eye_seperation * Npix * (A - kfar/16) / view_distance
            table.append(int(h/2))
        for i in range(0,height):
            for j in range (0,width):
                #print(i,j,DepthedImage[i,j])
                depth_level = int(DepthedImage[i,j])
                shift = table[depth_level]
                if j + shift -S >= 0 and j+shift-S < width:
                    warping_image[i][j + shift - S][0] = TexturedImage[i,j][0]
                    warping_image[i][j + shift - S][1] = TexturedImage[i,j][1]
                    warping_image[i][j + shift - S][2] = TexturedImage[i,j][2]
                elif j+shift -S >= 0 and j+shift-S >width:
                    warping_image[i+1][j + shift - S-i][0] = TexturedImage[i,j][0]
                    warping_image[i+1][j + shift - S-i][1] = TexturedImage[i,j][1]
                    warping_image[i+1][j + shift - S-i][2] = TexturedImage[i,j][2]

        return warping_image


    def warpingwith3D(self,TexturedImage,DepthedImage,CameraParameter):
        pass