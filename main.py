from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
arguments = argparse.ArgumentParser()
arguments.add_argument("-v", "--video",
                       help="path to the (optional) video file")
arguments.add_argument("-b", "--buffer", type=int, default=64,
                       help="max buffer size")
args = vars(arguments.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
lower_color_boundary = (0, 108, 101)
upper_color_boundary = (31, 167, 255)
trail = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
# otherwise, grab a reference to the video file
if not args.get("video", False):
    video = VideoStream(src=0).start()
else:
    video = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

while True:
    # grab current frame
    frame = video.read()

    # handle the frame for VideoCapture or VideoStream
    frame = frame[1] if args.get('video', False) else frame

    # check if end of video
    if frame is None:
        break

    # resizing, blurring and converting to HSV
    frame = imutils.resize(frame, width=900)
    blur = cv2.GaussianBlur(frame, (1, 1), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # remove imperfections on the ball
    mask = cv2.inRange(hsv, lower_color_boundary, upper_color_boundary)
    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=5)

    # detect the contour of the ball
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # check if at least one contour was found
    if len(contours) > 0:
        # find the largest contour and find the center of the circle
        max_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
        moments = cv2.moments(max_contour)
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))

        # draw the circle around the ball
        # update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the trail queue
    trail.appendleft(center)

    # ignore trail points whose value is None
    for i in range(1, len(trail)):
        if trail[i - 1] is None or trail[i] is None:
            continue

        # if the value of the trail points is not None
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, trail[i - 1], trail[i], (0, 0, 255), thickness)

    # show the frame
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'x' key is pressed, stop the loop
    if key == ord('x'):
        break

# handle the stopping of the webcam / video file
if not args.get('video', False):
    video.stop()
else:
    video.release()

# close all windows
cv2.destroyAllWindows()
