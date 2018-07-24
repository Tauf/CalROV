'''
Object detection and tracking with OpenCV
    ==> Turning a LED on detection and
    ==> Real Time tracking with Pan-Tilt servos 
    Based on original tracking object code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/
Adapted by Benjamin Li @Jun 28 2018
'''

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO
from time import sleep

#define Servos GPIOs
panServo = 27
tiltServo = 17

# initialize LED GPIO
redLed = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed, GPIO.OUT)

#position servos 
def positionServo (servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 200):
        panAngle += 10
        if panAngle > 140:
            panAngle = 140
        positionServo (panServo, panAngle)
        sleep(0.3)
 
    if (x > 230):
        panAngle -= 10
        if panAngle < 30:
            panAngle = 30
        positionServo (panServo, panAngle)
        sleep(0.3)

    if (y < 60):
        tiltAngle -= 10
        if tiltAngle < 60:
            tiltAngle = 60
        positionServo (tiltServo, tiltAngle)
 
    if (y > 200):
        tiltAngle += 10
        if tiltAngle > 170:
            tiltAngle = 170
        positionServo (tiltServo, tiltAngle)

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
'''
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
'''
vs = VideoStream(0).start()
time.sleep(2.0)

# define the lower and upper boundaries of the object
# to be tracked in the HSV color space
colorLower = (15,166,114)
colorUpper = (19,255,255) 

# Start with LED off
GPIO.output(redLed, GPIO.LOW)
ledOn = False

# Initialize angle servos at 90-90 position
global panAngle
panAngle = 60
global tiltAngle
tiltAngle =170

# positioning Pan/Tilt servos at initial position
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

# loop over the frames from the video stream
while True:
	# grab the next frame from the video stream, Invert 180o, resize the
	# frame, and convert it to the HSV color space
	frame = vs.read()
	frame = imutils.resize(frame, width=320,height=240)
	frame = imutils.rotate(frame, angle=180)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the object color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 1:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			# position Servo at center of circle
			mapServoPosition(int(x), int(y))
			
			# if the led is not already on, turn the LED on
			if not ledOn:
				GPIO.output(redLed, GPIO.HIGH)
				ledOn = True

	# if the ball is not detected, turn the LED off
	elif ledOn:
		GPIO.output(redLed, GPIO.LOW)
		ledOn = False

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	
	# if [ESC] key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
            break

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
positionServo (panServo, 130)
positionServo (tiltServo, 170)
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()
