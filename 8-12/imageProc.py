import cv2 as cv
import numpy as np
#import matplotlib as plt
import os
#import glob #Det kan godt være dette ikke virker som det skal?


imgFolderPath = ""
assert imgFolderPath is not None

#sortedimagepath = sorted(os.listdir(imgFolderPath))



img = cv.imread(cv.samples.findFile("starry_night.jpg"))

cv.imshow("Display window", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.imwrite("starry_night.png", img)














for filename in sortedimagepath:
    #Iterates for each file path, from the given folder path in imgFolderPath
    imagePath = os.path.join(imgFolderPath, filename)
    
    #Sets the image frame
    frame = cv.imread(imagePath, cv.IMREAD_GRAYSCALE)
    
    #Finds the size of the image, since OpenCV interacts with the image as a Numpy array.
    heigth, width, _ = frame.shape.index()
    
    #Starts the contouring function
    contours, _ = cv.findContours()

    #Defines empty list, too add all "found" contours
    contourDetections = []
    for cnt in contours:
        area = cv.contourArea    
    






