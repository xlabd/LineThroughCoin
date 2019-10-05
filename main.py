import numpy as np 
import cv2 
from skimage import morphology

'''Reading'''
img = cv2.imread('coin.jpg', 0)         #read
cv2.imshow('image', img)                #show
k = cv2.waitKey(0) & 0xFF               
if k == 27:  
    cv2.destroyAllWindows()             # wait for ESC key to exit

'''thresholding'''
ret, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
#cv2.imshow('Binary Threshold Inverted', thresh)            #show
#if cv2.waitKey(0) & 0xff == 27:  
#    cv2.destroyAllWindows()             # De-allocate any associated memory usage

'''closing- to make edges meet'''
kernel = np.ones((3, 3), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)                                       #morphology operation closing

'''fill holes'''
im_floodfill = closing.copy()           # Copy the thresholded image.
# Mask used to flood filling. Notice the size needs to be 2 pixels than the image.
h, w = closing.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8) 
cv2.floodFill(im_floodfill, mask, (0,0), 255);               # Floodfill from point (0, 0)
im_floodfill_inv = cv2.bitwise_not(im_floodfill)        # Invert floodfilled image
im_out = closing | im_floodfill_inv                             # Combine the two images to get the foreground.
#cv2.imshow("Foreground", im_out)                            # Display images.
#if cv2.waitKey(0) & 0xff == 27:  
#    cv2.destroyAllWindows()             # De-allocate any associated memory usage

'''destroy small holes'''
im_out = cv2.erode(im_out, None, iterations=8)
im_out = cv2.dilate(im_out, None, iterations=8)
#cv2.imshow("Holes removed", im_out)                            # Display images.
#if cv2.waitKey(0) & 0xff == 27:  
#    cv2.destroyAllWindows()             # De-allocate any associated memory usage

'''centroid'''
#blank image
height = np.size(img, 0)
width = np.size(img, 1)
centroids = np.zeros((height,width,3), np.uint8)
# find contours in the binary image
contours, hierarchy = cv2.findContours(im_out,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
   # calculate moments for each contour
    M = cv2.moments(c)
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(centroids, (cX, cY), 10, (255, 255, 255), -1)
cv2.imshow("Centroids", centroids)                      # Display images.
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()             # De-allocate any associated memory usage
    
''''''