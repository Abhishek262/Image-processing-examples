'''
Takes a blurred image, applies Wiener deconvolution to it and returns an unblurred image.
To get a colored image, takes individual R,G,B components, applies the filter over it
based on the parameters (chosen for each component).
Can be used for motion blur reduction.

'''

import cv2
import numpy as np
import os
import math
import csv
import cv2.aruco as aruco
from aruco_lib import *
import copy

codes_folder_path = os.path.abspath('.')
images_folder_path = os.path.abspath(os.path.join('..', 'Videos'))
generated_folder_path = os.path.abspath(os.path.join('..', 'Generated'))


def blur_edge(img, d=31):
    h, w  = img.shape[:2]
    img_pad = cv2.copyMakeBorder(img, d, d, d, d, cv2.BORDER_WRAP)
    img_blur = cv2.GaussianBlur(img_pad, (2*d+1, 2*d+1), -1)[d:-d,d:-d]
    y, x = np.indices((h, w))
    dist = np.dstack([x, w-x-1, y, h-y-1]).min(-1)
    w = np.minimum(np.float32(dist)/d, 1.0)
    return img*w + img_blur*(1-w)

def motion_kernel(angle, d, sz=65):
    kern = np.ones((1, d), np.float32)
    c, s = np.cos(angle), np.sin(angle)     
    A = np.float32([[c, -s, 0], [s, c, 0]])
    sz2 = sz // 2
    A[:,2] = (sz2, sz2) - np.dot(A[:,:2], ((d-1)*0.5, 0))
    kern = cv2.warpAffine(kern, A, (sz, sz), flags=cv2.INTER_CUBIC)
    return kern

def defocus_kernel(d, sz=65):
    kern = np.zeros((sz, sz), np.uint8)
    cv2 .motion(kern, (sz, sz), d, 255, -1, cv2.LINE_AA, shift=1)
    kern = np.float32(kern) / 255.0
    return kern


def process(ip_image):

    id_list = []
    #modifiable parameters for image cropping
    y=0
    x=0
    h=723
    w=1281
    crop_img =ip_image[y:y+h, x:x+w]
    ##cv2.imshow("cropped", crop_img)
    ip_image=crop_img
    want=ip_image
    blue= want[:,:,0]
    green= want[:,:,1]
    red= want[:,:,2]

    #ip_image = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    ip_image = np.float32(blue)/255.0

    #kernel parameters
    ang = np.deg2rad(90)
    d = 20
    noise = 10**(-0.1*30)

    img = blur_edge(ip_image)
    psf = motion_kernel(ang, d)
    IMG = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)
    psf /= psf.sum()
    psf_pad = np.zeros_like(ip_image)
    kh, kw = psf.shape
    psf_pad[:kh, :kw] = psf
    PSF = cv2.dft(psf_pad, flags=cv2.DFT_COMPLEX_OUTPUT, nonzeroRows = kh)
    PSF2 = (PSF**2).sum(-1)
    iPSF = PSF / (PSF2 + noise)[...,np.newaxis]
    RES = cv2.mulSpectrums(IMG, iPSF, 0)
    res = cv2.idft(RES, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )
    res = np.roll(res, -kh//2, 0)
    res = np.roll(res, -kw//2, 1)
    blue=res

    ip_image = np.float32(green)/255.0

    #kernel parameters
    ang = np.deg2rad(90)
    d = 20
    noise = 10**(-0.1*30)

    img = blur_edge(ip_image)
    psf = motion_kernel(ang, d)
    IMG = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)
    psf /= psf.sum()
    psf_pad = np.zeros_like(ip_image)
    kh, kw = psf.shape
    psf_pad[:kh, :kw] = psf
    PSF = cv2.dft(psf_pad, flags=cv2.DFT_COMPLEX_OUTPUT, nonzeroRows = kh)
    PSF2 = (PSF**2).sum(-1)
    iPSF = PSF / (PSF2 + noise)[...,np.newaxis]
    RES = cv2.mulSpectrums(IMG, iPSF, 0)
    res = cv2.idft(RES, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )
    res = np.roll(res, -kh//2, 0)
    res = np.roll(res, -kw//2, 1)
    green=res


    ip_image = np.float32(red)/255.0

    #kernel parameters
    ang = np.deg2rad(90)
    d = 20
    noise = 10**(-0.1*30)


    img = blur_edge(ip_image)
    psf = motion_kernel(ang, d)
    IMG = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)
    psf /= psf.sum()
    psf_pad = np.zeros_like(ip_image)
    kh, kw = psf.shape
    psf_pad[:kh, :kw] = psf
    PSF = cv2.dft(psf_pad, flags=cv2.DFT_COMPLEX_OUTPUT, nonzeroRows = kh)
    PSF2 = (PSF**2).sum(-1)
    iPSF = PSF / (PSF2 + noise)[...,np.newaxis]
    RES = cv2.mulSpectrums(IMG, iPSF, 0)
    res = cv2.idft(RES, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )
    res = np.roll(res, -kh//2, 0)
    res = np.roll(res, -kw//2, 1)
    red=res

    blue  = 255*blue
    green = 255*green
    red = 255*red


    color = cv2.merge([blue,green,red])
    cv2.waitKey(0)
    ip_image=color
	
    cv2.imwrite('temp.png',color)
    cx = cv2.imread('temp.png')
    ar_list = detect_Aruco(cx) 
    rs = calculate_Robot_State(cx,ar_list)
    a_lst = list(rs.values())
    aruco_info = []
    for ele in a_lst[0] : 
        aruco_info.append(ele)

    op_image = mark_Aruco(cx,ar_list)
    # aruco_info = rs[""]


    return op_image, aruco_info

def main(val):

    i = 1
    ## reading in video 
    cap = cv2.VideoCapture(images_folder_path+"/"+"ArUco_bot.mp4")
    ## getting the frames per second value of input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    ##print(fps)
    ## getting the frame sequence
    frame_seq = int(val)*fps
    ## setting the video counter to frame sequence
    cap.set(1,frame_seq)
    ## reading in the frame
    ret, frame = cap.read()
    ## verifying frame has content
    print(frame.shape)
    ## display to see if the frame is correct
    ##cv2.imshow("cropped", crop_img)
    ##frame=crop_img########
    ##cv2.imshow("window", frame)
    ##cv2.waitKey(0);
    ## calling the algorithm function
    op_image, aruco_info = process(frame)
    # saving the output in  a list variable
    line = [str(i), "Aruco_bot.jpg" , str(aruco_info[0]), str(aruco_info[3])]
    ## incrementing counter variable
    i+=1
    ## verifying all data
    print(line)
    ## writing to angles.csv in Generated folder without spaces
    with open(generated_folder_path+"/"+'output.csv', 'w') as writeFile:
        print("About to write csv")
        writer = csv.writer(writeFile)
        writer.writerow(line)
    # closing csv file    
    writeFile.close()

    os.remove('temp.png')
    cv2.imwrite('../Generated/aruco_with_id.png',op_image)


############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main(input("time value in seconds:"))
