import numpy as np 
import cv2 

img = cv2.imread('coin.jpg', 0)         #read
cv2.imshow('image', img)                #show
k = cv2.waitKey(0) & 0xFF               
if k == 27:  
    cv2.destroyAllWindows()             # wait for ESC key to exit

'''thresholding'''
ret, thresh2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('Binary Threshold Inverted', thresh2)            #show
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()             # De-allocate any associated memory usage

'''closing'''
kernel = np.ones((3, 3), np.uint8)
closing = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel, iterations=4)
    
'''fill holes'''
im_floodfill = thresh2.copy()           # Copy the thresholded image.
# Mask used to flood filling. Notice the size needs to be 2 pixels than the image.
h, w = thresh2.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
 
cv2.floodFill(im_floodfill, mask, (0,0), 255);               # Floodfill from point (0, 0)
im_floodfill_inv = cv2.bitwise_not(im_floodfill)        # Invert floodfilled image
im_out = thresh2 | im_floodfill_inv                             # Combine the two images to get the foreground.
cv2.imshow("Foreground", im_out)                            # Display images.
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()             # De-allocate any associated memory usage