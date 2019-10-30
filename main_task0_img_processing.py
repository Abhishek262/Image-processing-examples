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
    pass

def partC():
    pass

def partD():
    pass

partA()
partB()
partC()
partD()
