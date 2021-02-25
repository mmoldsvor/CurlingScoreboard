#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
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


#vancouver
red = np.uint8([[[199,61,64]]])
yellow = np.uint8([[[216,201,36]]])
outer = np.uint8([[[49,175,52]]])
inner = np.uint8([[[33,43,107]]])
maxValue = 255
lowH = 50
lowS = 92
lowV = 0
highS = 245
highV = maxValue
HMarg = 10
gaus = 29

stoneR = 30
radMarg = 7

innerR = 160
innerMarg = 7
outerR = 487
outerMarg = 7

#Convert to HSV
redHsv = cv2.cvtColor(red,cv2.COLOR_RGB2HSV)
yellowHsv = cv2.cvtColor(yellow,cv2.COLOR_RGB2HSV)
outerHsv = cv2.cvtColor(outer,cv2.COLOR_RGB2HSV)
innerHsv = cv2.cvtColor(inner,cv2.COLOR_RGB2HSV)


def colorTresh(img,H):
    """Create mask with given color, H"""

    hMin = H-HMarg
    hMax = H+HMarg
    imHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

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
    """Draw circle with given color image"""
    output = img.copy()
    # Draw circles that are detected. 
    color = tuple(color)
    if circles is not None:

        # Convert the circle parameters a, b and r to integers. 
        circles = np.uint16(np.around(circles))

        for pt in circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle. 
            cv2.circle(output, (a, b), r, color, 3)

            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(output, (a, b), 1, color, 3)

    return output


def showIm(name,img, scale):
    """resize and show image"""
    cv2.imshow(name,cv2.resize(img,(0,0),fx=scale,fy=scale))

def changeRadius(circles, reduceBy):
    for c in circles[0]:
        c[2] -= reduceBy
    return circles

def distToCenter(stone, house):
    """Calculating distance from middle of house to stones"""
    distx = house[0] - stone[0]
    disty = house[1] - stone[1]
    dist = np.sqrt(distx**2 + disty**2)-stoneR
    return dist

def midStones(stones,house,color,middleStones):
    """return list with stones inside house"""
    houseR = house[2]

    for stone in stones:
        dist = distToCenter(stone, house)
        if dist < houseR:
            #middleStones.append(np.ndarray.tolist(stone).append(")
            middleStones.append([dist,color])

    return middleStones


def getPoints(rCirc,yCirc,house):
    """return points and team"""
    mid = []
    midStones(rCirc,house,"red",mid)
    midStones(yCirc,house,"yellow",mid)
    midSort = sorted(mid)

    winner = midSort[0][1]
    score = 0
    for stone in midSort:
        if stone[1] != winner:
            break
        else:
            score += 1

    return winner, score


def main(image):
    redMask = colorTresh(image,int(redHsv[0,0,0]))
    yellowMask = colorTresh(image,int(yellowHsv[0,0,0]))
    outerMask = colorTresh(image,int(outerHsv[0,0,0]))
    innerMask = colorTresh(image,int(innerHsv[0,0,0]))

    redCircles = detectCircle(redMask,5,stoneR-radMarg,stoneR+radMarg)
    yellowCircles = detectCircle(yellowMask,5,stoneR-radMarg,stoneR+radMarg)
    outerCircle = detectCircle(outerMask,5,outerR-outerMarg,outerR+outerMarg)
    innerCircle = detectCircle(innerMask,5,innerR-innerMarg,innerR+innerMarg)

    output = drawCircles(image,(0,255,255),redCircles)
    output = drawCircles(output,(168,0,45),yellowCircles)
    output = drawCircles(output,(255,0,0),outerCircle)
    output = drawCircles(output,(0,255,100),innerCircle)

    winner, score = getPoints(redCircles[0],yellowCircles[0],outerCircle[0,0])

    showIm("out",output,0.5)
    cv2.waitKey(0)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image",help="path to imput image")
    args = vars(ap.parse_args())

    if args["image"]  == None:
        imPath = "curling.png"
    else:
        imPath = args["image"]

    image = cv2.imread(imPath)

    main(image)
