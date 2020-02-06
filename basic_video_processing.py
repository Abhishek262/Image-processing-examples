import cv2
import numpy as np
import os

def partA():
    vid = cv2.VideoCapture('../Videos/RoseBloom.mp4')
    suc,img = vid.read();
    frame_count = 0
    while suc:
        if (frame_count == 150):
            cv2.imwrite('../Generated/frame_as_6.jpg',img)
        suc,img = vid.read()
        frame_count += 1
    pass

def partB():
    img = cv2.imread('../Generated/frame_as_6.jpg',cv2.IMREAD_UNCHANGED)
    red = img[:,:,2]
    red_img = np.zeros(img.shape)
    red_img[:,:,2] = red;
    cv2.imwrite('../Generated/frame_as_6_red.jpg',red_img)
    pass

partA()
partB()
