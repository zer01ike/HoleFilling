from Tools import ReadYUV

yuv = ReadYUV.YUVTools()
yuv.setParamters(768, 1024, 300)
yuv.ReadYUV420("../DataSet/yuv/depth/Depth_balloons_1.yuv")
yuv.WriteImage("../DataSet/testSequence_depth/")