from sklearn.cluster import KMeans
import numpy as np

#Using the ICIP 2010's way to filling the disocusion in the depth map
#
#choose i which is not in the distortion area, calculate the M*M windows size area which i is
#the center of them. then find a j which is in this area and it's in the distortion area.
#calculate the k-means(k=2) to find the min and max in this area . using this value to overload j's
#value.
#

class DepthFilling() :
    def DepthFill(self, DepthImage, WindowSize):
        #step 1: choose i
        height, width = DepthImage.shape

        h_start = int(0+WindowSize/2)
        h_end = int(height - WindowSize/2)

        w_start = h_start
        w_end = int(width - WindowSize/2)
        height_count = 0
        width_count = 0

        times_count =0
        totally = (h_end-h_start) * (w_end - w_start)/32/32
        for i in range(h_start,h_end,int(WindowSize)):
            for j in range(w_start,w_end,int(WindowSize)):
                hole_count = 0
                sample = np.zeros((WindowSize * WindowSize, 2))
                # (i,j) is the center of the M*M area
                # get every value in this area and using K-means to cluster the min and the max

                for temp_i in range(int(i-WindowSize/2), int(i+WindowSize/2)):
                    for temp_j in range(int(j-WindowSize/2), int(j+WindowSize/2)):
                        #print(height_count, width_count)
                        if DepthImage[temp_i,temp_j] == 255:
                            hole_count +=1
                        sample[height_count * WindowSize + width_count][0] = DepthImage[temp_i, temp_j]
                        sample[height_count * WindowSize + width_count][1] = DepthImage[temp_i, temp_j]
                        width_count += 1
                    width_count = 0
                    height_count += 1
                height_count = 0

                sample_without_hole = np.zeros((sample.size-hole_count,2))
                count_without_hole = 0
                for x in range(0,int(sample.size/2)):
                    if sample[x][0] != 255 :
                        sample_without_hole[count_without_hole][0] = sample[x][0]
                        sample_without_hole[count_without_hole][1] = sample[x][1]
                        count_without_hole+=1

                est =  KMeans(2)
                est.fit(sample_without_hole)
                center = est.cluster_centers_
                if center[1][0] > center[0][0] :
                    c_min = center[0][0]
                else:
                    c_min = center[1][0]
                for temp_i in range(int(i-WindowSize/2), int(i+WindowSize/2)):
                    for temp_j in range(int(j-WindowSize/2), int(j+WindowSize/2)):
                        if DepthImage[temp_i,temp_j] == 255:
                            DepthImage[temp_i, temp_j] = int(DepthImage[i, j]) if DepthImage[i, j] <= c_min else int(c_min)
                times_count += 1
            print(str(round(times_count/totally*100,3))+"%"+"Processed")
        return DepthImage


    def testKmeans(self,DepthImage):
        height, width = DepthImage.shape
        #print(height,width,DepthImage[int(height/2), int(width/2)])
        sample=np.zeros((width*height,2))
        for i in range(0, height):
            for j in range(0, width):
                #calcute the hole image's min and max
                sample[i*height+j][0] = DepthImage[i,j]
                sample[i * height + j][1] = DepthImage[i, j]
        print(sample)
        est = KMeans(2)
        est.fit(sample)
        pred = est.cluster_centers_

        c_min = pred[1][0]
        c_max = pred[0][0]


        for i in range(0, height):
            for j in range(0, width):
                if DepthImage[i, j] == 255 :
                    DepthImage[i, j] = int(DepthImage[int(height/2), int(width/2)]) if DepthImage[int(height/2), int(width/2)]<=c_min else int(c_min)

        return DepthImage



