import numpy as np
# this is the class for 3D image processing
# which can make the a image to warp to a new place
# and contain 1D and 3D ways to do this
# 3D way need to be done.
#
# provided by zer0like<wangkai_like@163.com> at 5.4.2018
# #


class warping():
    def warpingwith1D(self, TexturedImage, DepthedImage):
        table = []
        knear = 0  # the near is 0
        kfar = 128  # the far is 128
        eye_seperation = 6  # means the seperation of the two eye is the 6cm
        view_distance = 800  # the view distance is 3m
        Npix = 320  # standard definition display to reduce the pararllex
        S = 25  # depth = 0, maxium shift .
        height, width, channels = TexturedImage.shape
        warping_image = np.zeros((height, width, 3), np.uint8)
        warping_depth_image = np.zeros((height, width, 1), np.uint8)
        for i in range(0, 256):
            A = i * (knear / 64 + kfar / 16) / 255
            h = -eye_seperation * Npix * (A - kfar / 16) / view_distance
            table.append(int(h / 2))
        for i in range(0, height):
            for j in range(0, width):
                # print(i,j,DepthedImage[i,j])
                depth_level = int(DepthedImage[i, j])
                shift = table[depth_level]
                if j + shift - S >= 0 and j + shift - S < width:
                    for s in range (0,3):
                        warping_image[i][j + shift - S][s] = TexturedImage[i, j][s]
                        #make the disclosure area with RGB = (200,200,200)
                        warping_image[i][j] = 200
                    warping_depth_image[i][j + shift - S] = DepthedImage[i, j]
                    # make the  of the area of the
                    warping_depth_image[i][j]= 255
                elif j + shift - S >= 0 and j + shift - S > width:
                    for s in range (0,3):
                        warping_image[i + 1][j + shift - S - i][s] = TexturedImage[i, j][s]
                        warping_image[i+1][j-i] = 200
                    warping_depth_image[i + 1][j + shift - S - i] = DepthedImage[i, j]
                    warping_depth_image[i + 1][j - i] = 255

        return warping_image, warping_depth_image

    def warpingwith3D(self, TexturedImage, DepthedImage, CameraParameter):
        pass
