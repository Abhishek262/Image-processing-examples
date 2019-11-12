###############################################################################
## Author: Team Supply Bot
## Edition: eYRC 2019-20
## Instructions: Do Not modify the basic skeletal structure of given APIs!!!
###############################################################################


######################
## Essential libraries
######################
import cv2
import numpy as np
import os
import math
import csv




########################################################################
## using os to generalise Input-Output
########################################################################
codes_folder_path = os.path.abspath('.')
images_folder_path = os.path.abspath(os.path.join('..', 'Images'))
generated_folder_path = os.path.abspath(os.path.join('..', 'Generated'))




############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################

def calc_dist(a,b) : 
    return math.sqrt((a[0] -  b[0])**2  +  (a[1] - b[1])**2 )


def process(ip_image):
    ###########################
    ## Your Code goes here
    ## placeholder image
    sector_image = np.ones(ip_image.shape,np.uint8)*255
    ## check value is white or not
    #To find radius of the circle

    mid_pixel_coord_x = ip_image.shape[0]//2 - 1
    mid_pixel_coord_y = ip_image.shape[1]//2 - 1


    mid_pixel = ip_image[mid_pixel_coord_x,mid_pixel_coord_y]

    rad1_start_pixel_x = 0
    rad2_start_pixel_y = mid_pixel_coord_y
    iter_pixel = 0
    # iter_pixel_x = mid_pixel_coord_x

    for i in range(mid_pixel_coord_x,ip_image.shape[1]) : 
        iter_pixel = (ip_image[i,mid_pixel_coord_y])
        if(iter_pixel[0] < 45 and iter_pixel[1] <45 and iter_pixel[2] <45) : 
            rad1_start_pixel_x = i
            break


    for i in range(rad1_start_pixel_x,ip_image.shape[1]) :
        iter_pixel = (ip_image[i,mid_pixel_coord_y])
        if(iter_pixel[0] > 150) : 
            rad2_start_pixel_x = i
            break

    rad1 = abs(rad1_start_pixel_x - mid_pixel_coord_x)
    rad2 = abs(rad2_start_pixel_x - mid_pixel_coord_x)
    mid = [mid_pixel_coord_x,mid_pixel_coord_y]
    #Choose all pixels inside the circle with radius rad2 and if they are white, make them black
    
    for x in range(0,ip_image.shape[1]) : 
        for y  in range(0,ip_image.shape[0]) : 
            if(calc_dist([x,y],mid) <= rad2 and ip_image[x,y][0] >250 and ip_image[x,y][1] > 250 and ip_image[x,y][2] > 250) : 
                if( (x<497 or x>525) and (y<497 or y>525)):
                    sector_image[x,y][0] = 30
                    sector_image[x,y][1] = 30
                    sector_image[x,y][2] = 30

    ## Your Code goes here
    ###########################
    # cv2.imshow("window", sector_image)
    # cv2.waitKey(0);
    return sector_image




    
####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Do not modify this code!!!
####################################################################
def main():
    ################################################################
    ## variable declarations
    ################################################################
    i = 1
    ## Reading 1 image at a time from the Images folder
    for image_name in os.listdir(images_folder_path):
        ## verifying name of image
        print(image_name)
        ## reading in image 
        ip_image = cv2.imread(images_folder_path+"/"+image_name)
        ## verifying image has content
        print(ip_image.shape)
        ## passing read in image to process function
        sector_image = process(ip_image)
        ## saving the output in  an image of said name in the Generated folder
        cv2.imwrite(generated_folder_path+"/"+"image_"+str(i)+"_fill_in.png", sector_image)
        i+=1


    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
