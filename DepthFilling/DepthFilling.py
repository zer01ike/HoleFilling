from sklearn.cluster import KMeans
from tqdm import tqdm
import numpy as np

# Using the ICIP 2010's way to filling the disocusion in the depth map
# choose i which is not in the distortion area, calculate the M*M windows size area which i is
# the center of them. then find a j which is in this area and it's in the distortion area.
# calculate the k-means(k=2) to find the min and max in this area . using this value to overload j's
# value.

# Attention: the kernel input must be odd number

# TODO: fix the tqdm error

class DepthFilling() :
    def __init__(self,depthimage,windowsize,stepsize):
        self.depthimage = depthimage
        self.windowsize = windowsize
        self.stepsize = stepsize
    def depthfill(self):

        # step 1: choose i
        height, width = self.depthimage.shape

        window_center = int(self.windowsize/2)

        vertical_equally = False
        horizontal_equally = False

        # calculate the edge if is not suitable to divide equally
        vertical_start = window_center
        vertical_end_for_range = self.get_edge(height, self.stepsize)*self.windowsize - window_center
        vertical_end_last_one = height - window_center
        #vertical_end = int(height - self.windowsize/2)

        horizontal_start = vertical_start
        #horizontal_end = int(width - self.windowsize/2)
        horizontal_end_for_range = self.get_edge(width,self.stepsize)*self.windowsize - window_center
        horizontal_end_last_one = width - window_center

        # counting the progress
        times_count = 0
        #totally = int((horizontal_end-horizontal_start+1) * (vertical_end - vertical_start+1)/self.stepsize/self.stepsize)



        # judge if it can be divided equally
        if vertical_end_for_range == vertical_end_last_one:
            vertical_equally = True
        
        if horizontal_end_for_range == horizontal_end_last_one:
            horizontal_equally = True


        total = (self.get_edge(height,self.stepsize)+(0 if vertical_equally else 1))*(self.get_edge(width,self.stepsize)+(0 if horizontal_equally else 1))
        # show process
        bar = tqdm(total=total)

        # first calculate the equally region
        for i in range(vertical_start, vertical_end_for_range, self.stepsize):
            for j in range(horizontal_start, horizontal_end_for_range, self.stepsize):
                self.get_kernel_content(i,j)
                times_count += 1
            bar.update(times_count)

        if vertical_equally == False :
            for i in range(horizontal_start,horizontal_end_for_range,self.stepsize):
                self.get_kernel_content(vertical_end_last_one-1,i)
                times_count += 1
            bar.update(times_count)
        if horizontal_equally == False :
            for i in range(vertical_start,vertical_end_for_range,self.stepsize):
                self.get_kernel_content(i,horizontal_end_last_one-1)
                times_count += 1
            bar.update(times_count)
        if vertical_equally == False and horizontal_equally == False :
            self.get_kernel_content(vertical_end_last_one-1,horizontal_end_last_one-1)
            times_count += 1
        bar.update(times_count)

        bar.close()
        return self.depthimage


    def get_edge(self,length,stepsize):
        i = 0
        while (True):
            current_edge = stepsize * i
            if current_edge > length :
                return i-1
            i += 1

    def get_kernel_content(self, i,j):
        # counting the
        vertical_count = 0
        horizontal_count = 0

        # count the hole numbers
        number_valid = 0

        # array to store the kernel content
        kernel_content = np.zeros(self.windowsize * self.windowsize)

        # (i,j) is the center of the M*M area
        # get every value in this area and using K-means to cluster the min and the max
        half = int(self.windowsize / 2)
        for kernel_v in range(i - half, i + half + 1):
            for kernel_h in range(j - half, j + half + 1):
                # print(vertical_count, horizontal_count)
                if self.depthimage[kernel_v, kernel_h] <= 250:
                    number_valid += 1
                index = vertical_count * self.windowsize + horizontal_count
                # print(index)
                kernel_content[index] = self.depthimage[kernel_v, kernel_h]
                horizontal_count += 1
            horizontal_count = 0
            vertical_count += 1
        vertical_count = 0

        kernel_without_hole = np.zeros(number_valid)

        count_without_hole = 0
        NoZero = False
        for x in range(0, int(kernel_content.size)):
            if kernel_content[x] <= 250:
                kernel_without_hole[count_without_hole] = kernel_content[x]
                count_without_hole += 1

                if kernel_content[x] != 0:
                    NoZero = True

        if NoZero == True:
            # print(kernel_without_hole)
            est = KMeans(2)
            est.fit(kernel_without_hole.reshape(-1, 1))
            center = est.cluster_centers_

            c_min = center[1] if center[1] < center[0] else center[0]
            # print(c_min)
            for kernel_v in range(i - half, i + half + 1):
                for kernel_h in range(j - half, j + half + 1):
                    if self.depthimage[kernel_v, kernel_h] >= 250:
                        self.depthimage[kernel_v, kernel_h] = int(self.depthimage[i, j]) if self.depthimage[i, j] <= c_min else int(
                            c_min)


    # test function...
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



