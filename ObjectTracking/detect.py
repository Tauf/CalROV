import cv2
import imutils
from imutils.video import VideoStream
import numpy as np
cap = VideoStream(0).start()
while(1):
    # Take each frame
    frame = cap.read()
    frame = imutils.rotate(frame, angle=180)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_orange = np.array([15,166,114]) #[1,3,222]
    upper_orange = np.array([19,255,255]) #[168,25,255]
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
