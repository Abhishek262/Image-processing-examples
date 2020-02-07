import cv2
import numpy as np
import os
import csv

img_path = r"../Images/"
gen_path = r"../Generated/"

def partA():
    
    file_names = os.listdir(img_path)
    img_obj = []
    for i in range(len(file_names)) :
        img_obj.append(cv2.imread(img_path + file_names[i]))

    #This list includes channels
    dimensions = [img.shape for img in img_obj]

    mid_pixel_intensity = []
    for i in range(len(img_obj)) : 
        imobj = img_obj[i]
        mid_pixel_x = dimensions[i][0] //2
        mid_pixel_y = dimensions[i][1] //2
        pixel = imobj[mid_pixel_x,mid_pixel_y]
        mid_pixel_intensity.append(pixel)

    print(mid_pixel_intensity)
    #To put it to a csv file
    with open("stats.csv",'w') as statsfile  :
        stats_writer = csv.writer(statsfile, delimiter = ',')
        for i in range(len(img_obj)) : 
            stats_writer.writerow([file_names[i],dimensions[i][0], dimensions[i][1],dimensions[i][2],
            mid_pixel_intensity[i][0], mid_pixel_intensity[i][1],mid_pixel_intensity[i][2]])

    os.rename("stats.csv",gen_path + "stats.csv" )

def partB():
    
    cat_img = cv2.imread(img_path + "cat.jpg") 
    red_img = cat_img.copy()
    red_img[:,:,0] = 0
    red_img[:,:,1] = 0
    cv2.imwrite(gen_path + 'cat_red.jpg',red_img)
    

def partC():
    flower_img = cv2.imread(img_path + "flowers.jpg") 
    b_channel,g_channel,r_channel = cv2.split(flower_img)
    alpha_channel = np.ones(r_channel.shape,dtype = r_channel.dtype) * 127
    flower_imga = cv2.merge((b_channel,g_channel,r_channel,alpha_channel))
    cv2.imwrite(gen_path + 'flowers_alpha.png', flower_imga)
    

def partD():
    horse_img = cv2.imread(img_path + "horse.jpg")
    b_channel,g_channel,r_channel = cv2.split(horse_img)
    i_channel = np.ones(b_channel.shape,dtype = b_channel.dtype)
    for i in range(0,b_channel.shape[0]):
        for j in range(0,b_channel.shape[1]) : 
            i_channel[i][j] = 0.3 * r_channel[i][j] + 0.59 * g_channel[i][j]  + 0.11 * b_channel[i][j]
    
    cv2.imwrite(gen_path + 'horse_gray.jpg',i_channel)


if __name__ == "__main__":
    partA()
    partB()
    partC()
    partD()
