from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# parsiranje argumenata
arguments = argparse.ArgumentParser()
arguments.add_argument("-v", "--video",
                       help="path to the (optional) video file")
arguments.add_argument("-b", "--buffer", type=int, default=64,
                       help="max buffer size")
args = vars(arguments.parse_args())

# donja i gornja granica za boju lopte (narandzasta)
# u HSV spektru boja
# dvostruko spregnuta lista u kojoj se cuvaju koordinate lopte za svaki frame
lower_color_boundary = (0, 108, 101)
upper_color_boundary = (31, 167, 255)
trail = deque(maxlen=args["buffer"])

# ako putanja do video snimka ne postoji inicijalizuj veb kameru
if not args.get("video", False):
    video = VideoStream(src=0).start()
else:
    video = cv2.VideoCapture(args["video"])

time.sleep(2.0)

while True:
    # procitaj frame sa videa
    frame = video.read()

    # u zavisnosti od toga da li imamo video ili veb kameru, dobavi frame
    frame = frame[1] if args.get('video', False) else frame

    # provera za kraj videa
    if frame is None:
        break

    # menjanje rezolucije, zamucivanje slike i prebacivanje u HSV spektar boja
    frame = imutils.resize(frame, width=900)
    blur = cv2.GaussianBlur(frame, (1, 1), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # pronalazimo boje koje upadaju u predefinisane granice
    mask = cv2.inRange(hsv, lower_color_boundary, upper_color_boundary)

    # detektujemo konturu lopte
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # proveravamo da li je neka lopta pronadjena
    if len(contours) > 0:
        # uzima se najveca pronadjena lopta
        max_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
        moments = cv2.moments(max_contour)
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))

        # crtanje kruga oko lopte za laksi prikaz funkcionalnosti
        # dodavanje koordinata lopte u listu za pracenje pozicije
        if radius > 30:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            trail.appendleft(center)

    # ignorisemo None vrednosti u listi
    for i in range(1, len(trail)):
        if trail[i - 1] is None or trail[i] is None:
            continue

        # crta se linija koja povezuje trenutnu i koordinatu iz proslog frame-a
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, trail[i - 1], trail[i], (0, 0, 255), thickness)

    # prikaz frame-a
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    # program prekida svoj rad pritiskom na 'x'
    if key == ord('x'):
        break

if not args.get('video', False):
    video.stop()
else:
    video.release()

cv2.destroyAllWindows()
