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
import copy






############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################


def process(ip_image):


    #to find coordinates of center 

    center_pixel_coords = []
    my = ip_image.shape[0]//2 - ip_image.shape[0]//7
    ny = ip_image.shape[0]//2 + ip_image.shape[0]//7
    
    mx  = ip_image.shape[1]//2 - ip_image.shape[1]//7
    nx = ip_image.shape[1]//2 + ip_image.shape[1]//7


    for i in range(my,ny):
        for j in range(mx,nx):
            if ip_image[i,j][2]>190 and ip_image[i,j][0]>190 and ip_image[i,j][1]>190:
                center_pixel_coords.append([i,j])

    print(center_pixel_coords)
  
    red_pixel_coords = []
    green_pixel_coords = []
    for i in range(0,ip_image.shape[0]):
        for j in range(0,ip_image.shape[1]):
            if ip_image[i,j][2]>100 and ip_image[i,j][0]>30 and ip_image[i,j][1]>30 and ip_image[i,j][2]<160 and ip_image[i,j][0]<80 and ip_image[i,j][1]<80:
                if i not in range(200,280) and j not in range(275,375):
                    red_pixel_coords.append([i,j])
            if ip_image[i,j][1]>180 and ip_image[i,j][2]>125 and ip_image[i,j][2]<155 and ip_image[i,j][0]<100 and ip_image[i,j][1]<230:
                green_pixel_coords.append([i,j])

    #finding centroids of the blobs created above
    centroid_r = [0,0]
    centroid_g = [0,0]
    centroid_c = [0,0]
        
    for element in center_pixel_coords : 
        centroid_c[0] += element[0]
        centroid_c[1] += element[1]

    for element in red_pixel_coords : 
        centroid_r[0] += element[0]
        centroid_r[1] += element[1]

    for element in green_pixel_coords : 
        centroid_g[0] += element[0]
        centroid_g[1] += element[1]

    
    centroid_c[0] = centroid_c[0]/len(center_pixel_coords)
    centroid_c[1] = centroid_c[1]/len(center_pixel_coords)

    centroid_r[0] = centroid_r[0]/len(red_pixel_coords)
    centroid_r[1] = centroid_r[1]/len(red_pixel_coords)

    centroid_g[0] = centroid_g[0]/len(green_pixel_coords)
    centroid_g[1] = centroid_g[1]/len(green_pixel_coords)

    #finally get the distances between each point
    mid = [centroid_c[0],centroid_c[1]]

    side_a = math.sqrt((centroid_r[0] -  mid[0])**2  +  (centroid_r[1] - mid[1])**2 )
    side_b = math.sqrt((centroid_g[0] -  mid[0])**2  +  (centroid_g[1] - mid[1])**2 )
    side_c = math.sqrt((centroid_r[0] -  centroid_g[0])**2  +  (centroid_r[1] - centroid_g[1])**2 )

    #cosine formula    side_b = math.sqrt((centroid_g[1] -  mid[0])**2  +  (centroid_g[1] - mid[1])**2 )

    cos_angle = (side_a**2  + side_b**2 - side_c**2)/(2*side_a*side_b)
    angle = math.acos(cos_angle)
    angle = math.degrees(angle)

    #for circles
    #find a point at the edge of the circle blob
    edge_point_y = min([j for j in center_pixel_coords[0]])
    # print("edge pt : " + str(edge_point_y))
    edge_pt_lst = [j for i,j in center_pixel_coords if(i==edge_point_y)]
    # print(edge_pt_lst)
    edge_point_x = math.ceil(sum(edge_pt_lst)/len(edge_pt_lst))
    # print(edge_point_x,edge_point_y)
    rad_c = math.sqrt((centroid_c[0] -edge_point_y )**2  +  (centroid_c[1] - edge_point_x)**2 )
    op_image = ip_image.copy()
    cv2.circle(op_image,(math.ceil(centroid_r[1]),math.ceil(centroid_r[0])),round(rad_c),(255,0,0),thickness=2)
    cv2.circle(op_image,(math.ceil(centroid_g[1]),math.ceil(centroid_g[0])),round(rad_c),(255,0,0),thickness=2)

    print([j[0] for j in red_pixel_coords])
    print([j[1] for j in red_pixel_coords])

    print(len(red_pixel_coords))
    print(len(green_pixel_coords))

    #to blit angle in the picture
    txt = "Angle : " + str(math.ceil(angle))
    cv2.putText(op_image,txt,(35,35),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow("w",op_image)
    cv2.waitKey(0)    


    return op_image



def process2(ip_image):
    n_image = ip_image.copy()
    # ip_image = cv2.GaussianBlur(ip_image,(3,3),0)
    hsv = cv2.cvtColor(ip_image, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([170,170,127]) 
    upper_red = np.array([180,254,190]) 

    lower_white = np.array([0,0,200]) 
    upper_white = np.array([180,40,268]) 

    lower_green = np.array([35, 100,150]) 
    upper_green = np.array([50,255,254]) 
  

    
    maskr = cv2.inRange(hsv, lower_red, upper_red) 
    maskw = cv2.inRange(hsv, lower_white, upper_white) 
    maskg = cv2.inRange(hsv, lower_green, upper_green) 

    #find centroid of white circle
    center_pixel_coords = []
    red_pixel_coords = []
    green_pixel_coords = []
    
    my = ip_image.shape[0]//2 - ip_image.shape[0]//5
    ny = ip_image.shape[0]//2 + ip_image.shape[0]//5
    
    mx  = ip_image.shape[1]//2 - ip_image.shape[1]//7
    nx = ip_image.shape[1]//2 + ip_image.shape[1]//7
    
    for i in range(my,ny):
        for j in range(mx,nx):
            if maskw[i,j] ==255:
                center_pixel_coords.append([i,j])

        #finding centroids of the blobs created above
    for i in range(0,maskr.shape[0]):
        for j in range(0,maskr.shape[1]):
            if i in range(180,300) and j in range(240,400) : 
                pass
            else:
                if maskr[i,j] ==255:
                    red_pixel_coords.append([i,j])

    for i in range(0,maskg.shape[0]):
        for j in range(0,maskg.shape[1]):
            if i in range(180,300) and j in range(240,400) : 
                pass
            else:
                if maskg[i,j] ==255:
                    green_pixel_coords.append([i,j])


    centroid_r = [0,0]
    centroid_g = [0,0]
    centroid_c = [0,0]
        
    for element in center_pixel_coords : 
        centroid_c[0] += element[0]
        centroid_c[1] += element[1]

    for element in red_pixel_coords : 
        centroid_r[0] += element[0]
        centroid_r[1] += element[1]

    for element in green_pixel_coords : 
        centroid_g[0] += element[0]
        centroid_g[1] += element[1]

    
    centroid_c[0] = centroid_c[0]/len(center_pixel_coords)
    centroid_c[1] = centroid_c[1]/len(center_pixel_coords)

    centroid_r[0] = centroid_r[0]/len(red_pixel_coords)
    centroid_r[1] = centroid_r[1]/len(red_pixel_coords)

    centroid_g[0] = centroid_g[0]/len(green_pixel_coords)
    centroid_g[1] = centroid_g[1]/len(green_pixel_coords)

    #finally get the distances between each point
    mid = [centroid_c[0],centroid_c[1]]

    # print(center_pixel_coords)
    # print()
    # print(red_pixel_coords)
    # print()
    # print(green_pixel_coords)
    # print()
    # cv2.imshow('maskw',maskw)
    # cv2.imshow('maskr',maskr)
    # cv2.imshow('maskg',maskg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    side_a = math.sqrt((centroid_r[0] -  mid[0])**2  +  (centroid_r[1] - mid[1])**2 )
    side_b = math.sqrt((centroid_g[0] -  mid[0])**2  +  (centroid_g[1] - mid[1])**2 )
    side_c = math.sqrt((centroid_r[0] -  centroid_g[0])**2  +  (centroid_r[1] - centroid_g[1])**2 )

    #cosine formula    side_b = math.sqrt((centroid_g[1] -  mid[0])**2  +  (centroid_g[1] - mid[1])**2 )

    cos_angle = (side_a**2  + side_b**2 - side_c**2)/(2*side_a*side_b)
    angle = math.acos(cos_angle)
    angle = math.degrees(angle)

    edge_point_y = min([j for j in center_pixel_coords[0]])
    # print("edge pt : " + str(edge_point_y))
    edge_pt_lst = [j for i,j in center_pixel_coords if(i==edge_point_y)]
    # print(edge_pt_lst)
    edge_point_x = math.ceil(sum(edge_pt_lst)/len(edge_pt_lst))
    # print(edge_point_x,edge_point_y)
    rad_c = math.sqrt((centroid_c[0] -edge_point_y )**2  +  (centroid_c[1] - edge_point_x)**2 )

    op_image = ip_image.copy()
    cv2.circle(n_image,(math.ceil(centroid_r[1]),math.ceil(centroid_r[0])),round(rad_c)+1,(255,0,0),thickness=2)
    cv2.circle(n_image,(math.ceil(centroid_g[1]),math.ceil(centroid_g[0])),round(rad_c)+1,(255,0,0),thickness=2)
    cv2.circle(n_image,(math.ceil(centroid_c[1]),math.ceil(centroid_c[0])),round(rad_c)+1,(255,0,0),thickness=2)
    

    print(len(red_pixel_coords))
    print(len(green_pixel_coords))

    #to blit angle in the picture
    txt = "Angle : " + str(math.ceil(angle))
    cv2.putText(n_image,txt,(35,35),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow("w",n_image)
    cv2.waitKey(0)    


    return op_image


####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Modify the image name as per instruction
####################################################################
def main():
    ################################################################
    ## variable declarations
    ################################################################
    i = 1
    ## reading in video 
    cap = cv2.VideoCapture('vid2.avi') #if you have a webcam on your system, then change 0 to 1
    ## getting the frames per second value of input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    ## setting the video counter to frame sequence
    cap.set(3, 640)
    cap.set(4, 480)
    ## reading in the frame
    ret, frame = cap.read()
    ## verifying frame has content
    print(frame.shape)
    # img = cv2.imread('pic.jpg')
    # process2(img)
    while(ret):
        ret, frame = cap.read()
        ## display to see if the frame is correct
        cv2.imshow("window", frame)
        cv2.waitKey(int(1000/fps));
        ## calling the algorithm function
        # cv2.imwrite("frame.jpg",op_image)

        op_image = process2(frame)
        cv2.imwrite("SB#9999_task3I.jpg",op_image)



    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
