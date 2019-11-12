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
def process(ip_image):
    ###########################
    ## Your Code goes here
    angle = 0.00
    #start from the center of the circle
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
 
    circle_rad  = (rad2-rad1)//2
    circle_angle_approx = (2 * circle_rad) / rad1
    circle_angle_approx = math.degrees(circle_angle_approx)

    #get all the red colored pixels in the pic
    red_pixel_coords = []
    green_pixel_coords = []
    for i in range(0,ip_image.shape[1]):
        for j in range(0,ip_image.shape[0]):
            if ip_image[i,j][2]>250 and ip_image[i,j][0]<10 and ip_image[i,j][1]<10:
                red_pixel_coords.append([i,j])
            if ip_image[i,j][1]>250 and ip_image[i,j][0]<10 and ip_image[i,j][2]<10:
                green_pixel_coords.append([i,j])

    #finding centroids of the blobs created above
    centroid_r = [0,0]
    centroid_g = [0,0]
    for element in red_pixel_coords : 
        centroid_r[0] += element[0]
        centroid_r[1] += element[1]

    for element in green_pixel_coords : 
        centroid_g[0] += element[0]
        centroid_g[1] += element[1]

    centroid_r[0] = centroid_r[0]/len(red_pixel_coords)
    centroid_r[1] = centroid_r[1]/len(red_pixel_coords)

    centroid_g[0] = centroid_g[0]/len(green_pixel_coords)
    centroid_g[1] = centroid_g[1]/len(green_pixel_coords)

    #finally get the distances between each point
    mid = [mid_pixel_coord_x,mid_pixel_coord_y]

    side_a = math.sqrt((centroid_r[0] -  mid[0])**2  +  (centroid_r[1] - mid[1])**2 )
    side_b = math.sqrt((centroid_g[0] -  mid[0])**2  +  (centroid_g[1] - mid[1])**2 )
    side_c = math.sqrt((centroid_r[0] -  centroid_g[0])**2  +  (centroid_r[1] - centroid_g[1])**2 )

    #cosine formula    side_b = math.sqrt((centroid_g[1] -  mid[0])**2  +  (centroid_g[1] - mid[1])**2 )

    cos_angle = (side_a**2  + side_b**2 - side_c**2)/(2*side_a*side_b)
    print("cos_angle " + str(cos_angle))
    angle = math.acos(cos_angle)
    angle = math.degrees(angle)

    ## Your Code goes here
    ###########################
    # cv2.imshow("window", ip_image)
    # cv2.waitKey(0);
    return angle




    
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
    line = []
    ## Reading 1 image at a time from the Images folder
    for image_name in os.listdir(images_folder_path):
        ## verifying name of image
        print(image_name)
        ## reading in image 
        ip_image = cv2.imread(images_folder_path+"/"+image_name)
        ## verifying image has content
        print(ip_image.shape)
        ## passing read in image to process function
        A = process(ip_image)
        ## saving the output in  a list variable
        line.append([str(i), image_name , str(A)])
        ## incrementing counter variable
        i+=1
    ## verifying all data
    print(line)
    ## writing to angles.csv in Generated folder without spaces
    with open(generated_folder_path+"/"+'angles.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(line)
    ## closing csv file    
    writeFile.close()



    

###########################################################################################
# main function
###########################################################################################
if __name__ == '__main__':
    main()


