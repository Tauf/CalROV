import cv2
import numpy as np
# Read the picure - The 1 means we want the image in BGR
img = cv2.imread('c1.jpg', 1) 
# resize imag to 20% in each axis
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
# convert BGR image to a HSV image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
# NumPy to create arrays to hold lower and upper range 
# The “dtype = np.uint8” means that data type is an 8 bit integer
lower_range = np.array([15,166,114], dtype=np.uint8) 
upper_range = np.array([19, 255, 255], dtype=np.uint8)
# create a mask for image
mask = cv2.inRange(hsv, lower_range, upper_range)
# display both the mask and the image side-by-side
cv2.imshow('mask',mask)
cv2.imshow('image', img)
# wait to user to press [ ESC ]
while(1):
  k = cv2.waitKey(0)
  if(k == 27):
    break
cv2.destroyAllWindows()
