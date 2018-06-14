from Tools import YUV
import cv2
from Warping import Warping
from DepthFilling import DepthFilling
from Sprite import Sprite
import numpy as np
from InitialHoleFilling import initial
from Tools import Hole_info
from Sprite import UpdateImage
from Refine import TextureRefine
import os

yuv_depth_path = "../DataSet/yuv/depth/BookArrival_Cam08_Depth.yuv"
yuv_texture_path = "../DataSet/yuv/Texture/BookArrival_Cam08.yuv"
saved_yuv_depth_path = "../DataSet/Sequence/Original/depth/"
saved_yuv_texture_path = "../DataSet/Sequence/Original/texture/"
saved_depthfill_path = "../DataSet/Sequence/DepthFill/"
saved_wapring_depth_path = "../DataSet/Sequence/Warped/depth/"
saved_wapring_texture_path = "../DataSet/Sequence/Warped/texture/"
saved_sprite_depth_path = "../DataSet/Sequence/Sprite/depth/"
saved_sprite_texture_path = "../DataSet/Sequence/Sprite/texture/"
saved_initial_texture_path = "../DataSet/Sequence/InitialFill/"
saved_update_depth_path = "../DataSet/Sequence/Update/depth/"
saved_update_texture_path = "../DataSet/Sequence/Update/texture/"
frame = 100


def processYUV(frame,yuv_depth_path,saved_yuv_depth_path,yuv_texture_path,saved_yuv_texture_path):
    # frame = 100
    yuv_depth = YUV.YUVtools()
    yuv_depth.setParamters(768, 1024, frame)
    yuv_depth.ReadYUV420(yuv_depth_path)
    yuv_depth.WriteImage(saved_yuv_depth_path)

    yuv_texture = YUV.YUVtools()
    yuv_texture.setParamters(768,1024,frame)
    yuv_texture.ReadYUV420(yuv_texture_path)
    yuv_texture.WriteImage(saved_yuv_texture_path)

def ReadImagetoList(frame):
    Depth_List = []
    Texture_List = []
    for i in range(0,frame):
        Depth_List.append(str(i)+".bmp")
        Texture_List.append(str(i)+".bmp")
    return Depth_List, Texture_List

def processwarping(Depth_List,Texture_List,frame,saved_yuv_depth_path,saved_yuv_texture_path,saved_wapring_depth_path,saved_wapring_texture_path):
    for i in range(0,frame):
        DepthedImg = cv2.imread(saved_yuv_depth_path+Depth_List[i], 0)
        TexturedImg = cv2.imread(saved_yuv_texture_path+Texture_List[i], 1)
        W1d = Warping.warping()
        output_txt_image, output_depth_image = W1d.warpingwith1D(TexturedImg, DepthedImg)
        cv2.imwrite(saved_wapring_depth_path+Depth_List[i],output_depth_image)
        cv2.imwrite(saved_wapring_texture_path+Texture_List[i],output_txt_image)
        print(i)

def processDetphfill(Depth_List,frame):
    f = open(saved_depthfill_path+"cmin.txt",'w')
    for i in range(0,frame):
        DepthedImg = cv2.imread(saved_wapring_depth_path+Depth_List[i], 0)
        DF = DepthFilling.DepthFilling(DepthedImg, 63, 63)
        depth_filled = DF.depthfill()
        cv2.imwrite(saved_depthfill_path+Depth_List[i], depth_filled)
        f.write(str(DF.get_median_cmin())+"\n")
    f.close()

def updateSprite(Depth_List,Texture_List,frame):
    f = open(saved_depthfill_path+"cmin.txt",'r')
    Sprite_bookArrival = Sprite.Sprite(768,1024)
    for i in range(0,frame):
        DepthedImg = cv2.imread(saved_wapring_depth_path+Depth_List[i], 0)
        TexturedImg = cv2.imread(saved_wapring_texture_path+Texture_List[i], 1)
        #read the cmin
        cmin = float(f.readline())
        #currentSprite = Sprite.Sprite(DepthedImg)
        Sprite_bookArrival.setGS(cmin, DepthedImg, TexturedImg)
        cv2.imwrite(saved_sprite_depth_path+Depth_List[i], Sprite_bookArrival.getG())
        cv2.imwrite(saved_sprite_texture_path+Texture_List[i], Sprite_bookArrival.getS())
        print(str(i)+":processing")

def initallFill(Texture_List,frame):
    hole = np.array([255, 255, 255])
    for i in range(0,frame):
        TexturedImg = cv2.imread(saved_wapring_texture_path + Texture_List[i], 1)
        a = initial.Initial()
        a.laplacian(TexturedImg, hole)
        cv2.imwrite(saved_initial_texture_path+Texture_List[i], TexturedImg)
        print(str(i) + ":processing")


# need to be examed
def updateImage(Depth_List,Texture_List,frame):
    hole = np.array([255,255,255])
    for i in range(0,2):
        TextureImage = saved_wapring_texture_path+Texture_List[i]
        DepthImage = saved_wapring_depth_path+Depth_List[i]
        DepthSprite = saved_sprite_depth_path+Depth_List[i]
        TextureSprite =saved_sprite_texture_path+Texture_List[i]
        B=5

        holeLoc = Hole_info.Hole(saved_wapring_texture_path+Texture_List[i], hole)
        holeLoc.findLoc()
        HoleList = holeLoc.getLoc()
        a = UpdateImage.updateImage(TextureImage,DepthImage,DepthSprite,TextureSprite,B,HoleList)
        cv2.imwrite(saved_update_texture_path+Texture_List[i],a.getTextureImage())




def refineImage():
    hole = np.array([255, 255, 255])
    holeLoc = Hole_info.Hole(saved_wapring_texture_path + Texture_List[0], hole)
    holeLoc.findLoc()
    HoleList = holeLoc.getLoc()
    a = TextureRefine.TextureRefine(saved_wapring_texture_path+Texture_List[0],saved_initial_texture_path+Texture_List[0],saved_depthfill_path+Depth_List[0],HoleList)
    result = a.updateImage(9)
    cv2.imwrite("test_final.bmp",result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def generate_daset():
    yuv_depth_path = "J:/DataSet/BookArrival_Cam08/yuv/depth/BookArrival_Cam08_Depth.yuv"
    yuv_texture_path = "J:/DataSet/BookArrival_Cam08/yuv/Texture/BookArrival_Cam08.yuv"
    saved_yuv_depth_path = "J:/DataSet/BookArrival_Cam08/Original/depth/"
    saved_yuv_texture_path = "J:/DataSet/BookArrival_Cam08/Original/texture/"
    saved_wapring_texture_path = "J:/DataSet/BookArrival_Cam08/Warped/"
    saved_wapring_depth_path = "J:/DataSet/BookArrival_Cam08/Warped/depth/"
    frame = 100
    Depth_List, Texture_List = ReadImagetoList(frame)

    processYUV(frame,yuv_depth_path,saved_yuv_depth_path,yuv_texture_path,saved_yuv_texture_path)
    processwarping(Depth_List,Texture_List,frame,saved_yuv_depth_path,saved_yuv_texture_path,saved_wapring_depth_path,saved_wapring_texture_path)



if __name__ == '__main__':
    #Depth_List, Texture_List = ReadImagetoList()
    #step 1
    #processYUV()

    #step 2
    #processwarping(Depth_List,Texture_List,frame)

    #step 3
    #processDetphfill(Depth_List,frame)

    #step 4
    #updateSprite(Depth_List,Texture_List,frame)

    #step 5
    #updateImage(Depth_List,Texture_List,frame)

    #step 6
    #initallFill(Texture_List,frame)

    #step 7
    #refineImage()
    generate_daset()