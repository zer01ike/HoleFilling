## TODO LIST :
- [x] Warping Process
- [x] Detph Fill
- [x] Sprite Update
    -[ ] Remember the hole location
- [ ] Image Update
- [x] Initial Fill
- [ ] Texture Refine
    


## paper's Assumption
1. BG(BackGround) is static 
2. For the moving BG, motion estimation is required to compensate the BG motion, then can use this function to filling the hole.



## input paramater
a video with associated depth map

## steps
* [step 1](#step-1) : Warping process 
* [step 2](#step-2) : Depth Fill
* [step 3](#step-3) : Sprite Update
* [step 4](#step-4) : Image Update
* [step 5](#step-5) : Initial Fill 

## step 1 
This is the algorithm to generate the a 3D image warping image and it's associated depth map, there have distortion area in both Warpied image and it's associated depth map 

see more detail in package `Warping` 

## step 2
Depth Fill is the pre-process of the depth map, which can fill the distortion area of the depth map with K-means Algorithm.

It's purpose is to separate the FG(foreground) and the BG(background).

Choose i's neighborhood which is like a M * N squared area. using K-means(K=2) to cluster those pixel's into to region. then we can get the cluster center named `c_min` and `c_max`

Then just do a judge function to change the i's value. If it is big than `C_min`, it will be `C_min`. If it is less than `C_min`, it will not change. See more detail in package 'DepthFilling' and the paper.

## step 3
`Sprite update` contain the BG sprite updation and DM sprite updation.

 BG and DM sprite are only one in whole process. just to calculate the median `C_min` and the do judge function to distribute the pixel which is needed to store in the Sprite 

## step 4

Need to be done 

## step 5
initial Filling contains two method, filling small holes just to using Laplace equation to fill. Fill large hole is using author's previous work( :sob: **I don't reproduce this work**)

## step 6
Texture refinement need to be done 

