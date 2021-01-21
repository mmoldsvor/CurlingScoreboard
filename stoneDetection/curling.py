#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 torje <torje@torje-ubuntu>
#
# Distributed under terms of the MIT license.

"""
Program for tracking curling stones
"""

import cv2
import imutils
import argparse
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s-  %(message)s')
logging.debug('Start of program')

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",help="path to imput image")
args = vars(ap.parse_args())

if args["image"]  == None:
    imPath = "curling.png"
else:
    imPath = args["image"]

image = cv2.imread(imPath)

windowDetectionName = 'Object Detection'
lowHName = 'Low H'
lowSName = 'Low S'
lowVName = 'Low V'
highHName = 'High H'
highSName = 'High S'
highVName = 'High V'
HName = "H"
HMargName = "H margin"
gausName = "Gaus"

maxValue = 255
maxValueH = 360//2
lowH = 50
lowS = 100
lowV = 100
highH = maxValueH
highS = maxValue
highV = maxValue
H = 25
HMarg = 10
gaus = 7
gausMax = 100

cv2.namedWindow(windowDetectionName)

def onTrackbar(x):
    pass

def makeTrackbar():

    cv2.createTrackbar(HName,windowDetectionName,H,maxValueH,onTrackbar)
    cv2.createTrackbar(HMargName,windowDetectionName,HMarg,maxValueH//2,onTrackbar)
    cv2.createTrackbar(lowHName,windowDetectionName,lowH,maxValueH,onTrackbar)
    cv2.createTrackbar(highHName,windowDetectionName,highH,maxValueH,onTrackbar)
    cv2.createTrackbar(lowSName,windowDetectionName,lowS,maxValue,onTrackbar)
    cv2.createTrackbar(highSName,windowDetectionName,highS,maxValue,onTrackbar)
    cv2.createTrackbar(lowVName,windowDetectionName,lowV,maxValue,onTrackbar)
    cv2.createTrackbar(highVName,windowDetectionName,highV,maxValue,onTrackbar)
    cv2.createTrackbar(gausName,windowDetectionName,gaus,gausMax,onTrackbar)

def getTrackbar():
    H = cv2.getTrackbarPos(HName,windowDetectionName)
    HMarg = cv2.getTrackbarPos(HMargName,windowDetectionName)

    hMin = H-HMarg
    hMax = H+HMarg

    cv2.setTrackbarPos(lowHName,windowDetectionName,hMin)
    cv2.setTrackbarPos(highHName,windowDetectionName,hMax)

    lowH = cv2.getTrackbarPos(lowHName,windowDetectionName)
    highH = cv2.getTrackbarPos(highHName,windowDetectionName)
    lowS = cv2.getTrackbarPos(lowSName,windowDetectionName)
    highS = cv2.getTrackbarPos(highSName,windowDetectionName)
    lowV = cv2.getTrackbarPos(lowVName,windowDetectionName)
    highV = cv2.getTrackbarPos(highVName,windowDetectionName)
    gaus = cv2.getTrackbarPos(gausName,windowDetectionName)

    if gaus % 2 == 0:
        gaus+=1

    return hMin,hMax,lowS,highS,lowV,highV,gaus


def colorTresh(img,H):
    HMarg = cv2.getTrackbarPos(HMargName,windowDetectionName)
    hMin,hMax,lowS,highS,lowV,highV,gaus = getTrackbar()

    hMin = H-HMarg
    hMax = H+HMarg
    imHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #gausIm = cv2.GaussianBlur(imHsv,(gaus,gaus),0)

    if hMin < 0:
        clrTreshLower =cv2.inRange(imHsv,(hMin%maxValueH,lowS,lowV),(maxValueH,highS,highV))
        clrTreshUp = cv2.inRange(imHsv,(0,lowS,lowV),(hMax,highS,highV))
        clrTresh = clrTreshLower | clrTreshUp
    elif hMax > maxValueH:
        clrTreshLower = cv2.inRange(imHsv,(hMin,lowS,lowV),(maxValueH,highS,highV))
        clrTreshUp = cv2.inRange(imHsv,(0,lowS,lowV),(hMax%maxValueH,highS,highV))
        clrTresh = clrTreshLower | clrTreshUp
    else:
        clrTresh = cv2.inRange(imHsv,(hMin,lowS,lowV),(hMax,highS,highV))


    gausMask = cv2.GaussianBlur(clrTresh,(gaus,gaus),0)
    output = cv2.bitwise_and(gausMask,gausMask,mask=clrTresh)

    return gausMask

def detectCircle(img,gausSize,minR,maxR):
    """Detect circle from image within minR and maxR"""
    if len(img.shape)>2:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    grayGaus = cv2.GaussianBlur(gray,(gausSize,gausSize),0)

    # Apply Hough transform on the blurred image. 
    circles = cv2.HoughCircles(grayGaus,cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                               param2 = 30, minRadius = minR, maxRadius = maxR)
    return circles

def drawCircles(img,color,circles):
    output = img.copy()
    # Draw circles that are detected. 
    #logging.debug(str(color)+str(type(color[0])))
    color = tuple(color)
    #logging.debug(str(color)+str(type(color[0])))
    if circles is not None:

        # Convert the circle parameters a, b and r to integers. 
        circles = np.uint16(np.around(circles))

        for pt in circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle. 
            cv2.circle(output, (a, b), r, color, 2)

            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(output, (a, b), 1, color, 3)

    return output




makeTrackbar()
red = (152,0,0)
yellow = (199,180,0)
redAr = np.uint8([[np.asarray(red)]])
yellowAr = np.uint8([[np.asarray(yellow)]])
redHsv = cv2.cvtColor(redAr,cv2.COLOR_RGB2HSV)
yellowHsv = cv2.cvtColor(yellowAr,cv2.COLOR_RGB2HSV)
outer = np.uint8([[[2,114,127]]])
inner = np.uint8([[[195,12,32]]])
outerHsv = cv2.cvtColor(outer,cv2.COLOR_RGB2HSV)
innerHsv = cv2.cvtColor(inner,cv2.COLOR_RGB2HSV)

while(True):
    #detectCircle(image,gaus,15,100)
    #detectCircle(image,gaus,75,140)
    redMask = colorTresh(image,int(redHsv[0,0,0]))
    yellowMask = colorTresh(image,int(yellowHsv[0,0,0]))

    outerMask = colorTresh(image,int(outerHsv[0,0,0]))
    innerMask = colorTresh(image,int(innerHsv[0,0,0]))

    edges = imutils.auto_canny(image)
    #cv2.imshow("CV-edge",outerMask)

    redCircles = detectCircle(redMask,5,15,35)
    yellowCircles = detectCircle(yellowMask,5,15,35)
    output = drawCircles(image,(0,255,255),redCircles)
    output = drawCircles(output,(168,0,45),yellowCircles)

    outerCircle = detectCircle(outerMask,5,75,400)
    drawouter = drawCircles(image,(255,0,0),outerCircle)

    innerCircle = detectCircle(innerMask,5,80,150)
    drawinner = drawCircles(image,(0,255,0),innerCircle)
    output = drawCircles(output,(0,255,100),innerCircle)

    #cv2.imshow("CV-outer",drawinner)
    cv2.imshow("CV-output",output)


    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break
