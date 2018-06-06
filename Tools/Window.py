import numpy as np
'''
window class is to handle the get an area value of a specific area of the image 
'''

class window():
    '''
    i_height = input height
    i_width = input width
    w_height = window height
    w_width = window width
    '''
    def __init__(self):
        pass

    def setWindowParamater(self,height,width):
        self.w_width = width
        self.w_height = height

    def setRegionParamater(self,height,width):
        self.i_height = height
        self.i_width = width

    def setStepParamater(self,stepsize):
        self.stepsize = stepsize
        
    def setRegionParamater(self,regionparamater):
        self.regionparamater = regionparamater
    

    def _check(self):
        '''
        check if the the window is ok to get value
        :return: True or false
        '''
        if self.w_height > self.i_height : return False
        if self.w_width > self.i_width : return False
        return True

    def _divisible(self):
        '''
        check if the window will be diveisibe of the picture with it's stepsize
        :return: True,True;True,Flase;...represent for height and width
        '''
        h_divisible = False
        w_divisible = False

        if self.stepsize == 1 : return True,True

        if not (self.i_height - self.w_height) % self.stepsize :
            h_divisible = True

        if not (self.i_width - self.w_width) % self.stepsize :
            w_divisible = True

        return h_divisible,w_divisible

    def _Windowindexs(self):
        '''
        get the index of every window
        and set it into the list to provide the loc of every block for futher pocess
        :return:
        '''
        h_divisible, w_divisible = self._divisible()
        height_index = np.arange(self.i_height)
        width_index = np.arange(self.i_width)

        height_index_slice = height_index[::self.w_height]
        width_index_slice = width_index[::self.w_width]

        self.indexList = []
        if not h_divisible :
            #if h can't be divisible add one data
            #np.append(height_index_slice,self.i_height-self.w_height)
            height_index_slice[-1] =self.i_height - self.w_height
        if not w_divisible :
            width_index_slice[-1] = self.i_width - self.w_width

        for i in height_index_slice:
            for j in width_index_slice:
                self.indexList.append({'x':i,'y':j})

        return self.indexList
    
    def Regionindexs(self,center,):
        '''
        calculate the regionsIndex list 
        :return: 
        '''
        index = self.CentertoRegionIndex(center)
        self.i_width = self.w_width * self.regionparamater
        self.i_height = self.w_height * self.regionparamater


        self._Windowindexs()
        # need a way to check the window index is useful
        self._checkindexList()

        return self.indexList


    def _checkindexList(self):
        for i in self.indexList:
            if i['x'] < 0 or i['x'] > self.i_height : self.indexList.remove(i)
            if i['y'] < 0 or i['y'] > self.i_width : self.indexList.remove(i)


    def getWindow(self,i,j):
        window = []
        for h in range(0,self.stepsize):
            for w in range(0,self.stepsize):
                window.append({'x':i+h,'y':j+w})
        return window

    def IndextoCenter(self,index):
        pass

    def CentertoIndex(self,center):
        pass
    
    def CentertoRegionIndex(self,center):
        '''
        calculate the regionIndex from the center location
        :param center: the location of the center
        :return: 
        '''
        
        x_temp = int(center['x'] - self.w_height * int(self.regionparamater/2))
        y_temp = int(center['y'] - self.w_width * int(self.regionparamater/2))
        
        x=0 if x_temp < 0 else x_temp
        y=0 if y_temp < 0 else y_temp
        
        return {'x':x,'y':y}