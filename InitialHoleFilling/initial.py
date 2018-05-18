# encoding = utf_8
class Initial:
    def __init__(self):
        pass

    # this is the laplacian function to initial the hole of a warpped image which the hole size less than 50 pixel
    def laplacian(self,TexturedImage,hole_value):
        self.height, self.width, channel= TexturedImage.shape
        for i in range(0, self.height):
            for j in range(0,self.width):
                if (TexturedImage[i,j] == hole_value).all() :
                    #using laplacian 010 141 010
                    self.calculate(i,j,TexturedImage)

    def calculate(self,i,j,TexturedImage):
        # judge if it has 3*3 block
        if i - 1 <0 or j-1<0 : return
        if i + 1 > self.height-1 or j+1 > self.width-1 : return

        # if it is calculateable
        for c in range(0,3):
            TexturedImage[i,j][c]= int ((int(TexturedImage[i,j-1][c])+int(TexturedImage[i,j+1][c])+int(TexturedImage[i-1,j][c])+int(TexturedImage[i+1,j][c]))/4)

        return