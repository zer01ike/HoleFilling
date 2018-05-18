from Tools import YUV

yuv = YUV.YUVtools()
yuv.setParamters(768, 1024, 2)
yuv.ReadYUV420("../DataSet/yuv/depth/BookArrival_Cam08_Depth.yuv")
yuv.WriteImage("../main/Sequence/Original/depth")