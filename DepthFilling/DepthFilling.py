from sklearn.cluster import KMeans
import numpy as np

# Using the ICIP 2010's way to filling the disocusion in the depth map
# choose i which is not in the distortion area, calculate the M*M windows size area which i is
# the center of them. then find a j which is in this area and it's in the distortion area.
# calculate the k-means(k=2) to find the min and max in this area . using this value to overload j's
# value.

# Attention: the kernel input must be odd number

class DepthFilling() :

    def depthfill(self, depthimage, windowsize, stepsize):
        # step 1: choose i
        height, width = depthimage.shape

        vertical_start = int(0 + windowsize/2)
        vertical_end = int(height - windowsize/2)

        horizontal_start = vertical_start
        horizontal_end = int(width - windowsize/2)

        #counting the
        vertical_count = 0
        horizontal_count = 0

        # counting the progress
        times_count = 0
        totally = (horizontal_end-horizontal_start) * (vertical_end - vertical_start)/stepsize/stepsize
        
        for i in range(vertical_start, vertical_end, stepsize):
            for j in range(horizontal_start, horizontal_end, stepsize):
                # count the hole numbers
                number_valid = 0
                
                # array to store the kernel content  
                kernel_content = np.zeros(windowsize * windowsize)
                
                # (i,j) is the center of the M*M area
                # get every value in this area and using K-means to cluster the min and the max
                half = int(windowsize/2)
                for kernel_v in range(i-half, i+half+1):
                    for kernel_h in range(j-half, j+half+1):
                        #print(vertical_count, horizontal_count)
                        if depthimage[kernel_v,kernel_h] <= 250:
                            number_valid += 1
                        index = vertical_count * windowsize + horizontal_count
                        #print(index)
                        kernel_content[index] = depthimage[kernel_v, kernel_h]
                        horizontal_count += 1
                    horizontal_count = 0
                    vertical_count += 1
                vertical_count = 0
                
                kernel_without_hole = np.zeros(number_valid)

                count_without_hole = 0
                NoZero = False
                for x in range(0, int(kernel_content.size)):
                    if kernel_content[x] <= 250 :
                        kernel_without_hole[count_without_hole] = kernel_content[x]
                        count_without_hole += 1

                        if kernel_content[x] !=0 :
                            NoZero = True

                if NoZero == True:
                    #print(kernel_without_hole)
                    est =  KMeans(2)
                    est.fit(kernel_without_hole.reshape(-1,1))
                    center = est.cluster_centers_

                    c_min = center[1] if center[1] < center[0] else center[0]
                    #print(c_min)
                    for kernel_v in range(i-half, i+half+1):
                        for kernel_h in range(j-half, j+half+1):
                            if depthimage[kernel_v,kernel_h] >=250:
                                depthimage[kernel_v, kernel_h] = int(depthimage[i, j]) if depthimage[i, j] <= c_min else int(c_min)
                times_count += 1

            print(str(round(times_count/totally*100,3))+"%"+"Processed")
        return depthimage


    def testKmeans(self,depthimage):
        height, width = depthimage.shape
        #print(height,width,depthimage[int(height/2), int(width/2)])
        sample=np.zeros(width*height)
        for i in range(0, height):
            for j in range(0, width):
                #calcute the hole image's min and max
                sample[i*height+j] = depthimage[i,j]
        print(sample)
        est = KMeans(2)
        est.fit(sample.reshape(-1,1))
        pred = est.cluster_centers_

        print(pred)

        c_min = pred[1] if pred[1]<pred[0] else pred[0]


        for i in range(0, height):
            for j in range(0, width):
                if depthimage[i, j] >= 250 :
                    depthimage[i, j] = int(depthimage[int(height/2), int(width/2)]) if depthimage[int(height/2), int(width/2)]<=c_min else int(c_min)

        return depthimage



