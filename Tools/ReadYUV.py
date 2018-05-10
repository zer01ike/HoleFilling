# this is the tool to read YUV video array and convert to RGB mode
# saving it in the memory
import struct

import cv2
import numpy as np

class YUVTools():

    def setParamters(self, height=0,width=0,frame =0):
        self.height = height
        self.width = width
        self.frame = frame
        self.RGB_video = []

    # read a YUV 4:2:0 file ,and it's  byte array is look like yyyyuuvv.
    def ReadYUV420(self,path):
        videofile = open(path,'rb')
        content = videofile.read()
        videoarray = struct.unpack(len(content)*'B',content)
        videofile.close()

        frame_block = int(self.width * self.height * 3 / 2)
        #RGB_video = []
        for i in range(0, self.frame):
            #videoarray.seek(frame_block * i,0)
            # get the Y and U and V
            frame_size = self.height * self.width
            Y_start = i * frame_block
            Y_end = Y_start + frame_size

            Y = videoarray[Y_start:Y_end]
            Y = np.reshape(Y, (self.height, self.width))

            s = Y_end
            e = s+int(frame_size/4)
            U = videoarray[s:e]
            U = np.repeat(U, 2, 0)
            U = np.reshape(U, (int(self.height / 2), int(self.width)))
            U = np.repeat(U, 2, 0)

            s = e
            e = e+int(frame_size/4)
            V = videoarray[s:e]
            V = np.repeat(V, 2, 0)
            V = np.reshape(V, (int(self.height / 2), int(self.width)))
            V = np.repeat(V, 2, 0)

            RGBMatrix = (np.dstack([Y, U, V])).astype(np.uint8)
            RGBMatrix = cv2.cvtColor(RGBMatrix, cv2.COLOR_YUV2BGR, 3)
            self.RGB_video.append(RGBMatrix)
        return self.RGB_video

    # wirte this self.RGB_video to a opencv video stream and write to file
    def WriteVideo(self,path):
        pass
    # write image to the diectory
    def WriteImage(self,path):
        count = 0
        for i in range(0,self.frame):
            if self.RGB_video == [] :
                return 0
            cv2.imwrite(path+str(i)+'.jpg',self.RGB_video[i])
            count +=1
        return count

