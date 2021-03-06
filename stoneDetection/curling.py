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
import json
import requests
import random


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s-  %(message)s')
logging.debug('Start of program')

camId = 1
SITE_URL = "https://gruppe13.innovasjon.ed.ntnu.no/sendPos/"+str(camId)+"/" # Where to send data.


#vancouver
red = np.uint8([[[199,61,64]]])
yellow = np.uint8([[[216,201,36]]])
outer = np.uint8([[[49,175,52]]])
inner = np.uint8([[[33,43,107]]])
maxValue = 255
maxValueH = 360//2
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

minDist = 10

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

    if circles is None:
        return None
    else:
        return circles[0]

def drawCircles(img,color,circles):
    """Draw circle with given color image"""
    output = img.copy()
    # Draw circles that are detected. 
    color = tuple(color)
    if circles is not None:

        # Convert the circle parameters a, b and r to integers. 
        circles = np.uint16(np.around(circles))

        for pt in circles:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle. 
            cv2.circle(output, (a, b), r, color, 3)

            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(output, (a, b), 1, color, 5)

    return output


def showIm(name,img, scale):
    """resize and show image"""
    cv2.imshow(name,cv2.resize(img,(0,0),fx=scale,fy=scale))

def changeRadius(circles, scale):
    for c in circles:
        c[2] *= scale
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
    if stones is not None:
        for stone in stones:
            dist = distToCenter(stone, house)
            distToHouse = abs(dist - houseR)
            if distToHouse < minDist:
                print("LITEN AVSTAND TIL BOET:",distToHouse)
            if dist < houseR:
                middleStones.append([dist,color])



def calcPoints(rCirc,yCirc,house):
    """return points and team"""
    mid = []
    midStones(rCirc,house,"red",mid)
    midStones(yCirc,house,"yellow",mid)
    midSort = sorted(mid)

    if len(mid) == 0:
        return "ingen", 0


    winner = midSort[0][1]
    score = 0
    prevDist = 0
    for stone in midSort:
        if stone[1] != winner:
            dist = stone[0]-prevDist
            print("Forskjell mellom steinene:",dist)
            if dist < minDist:
                print("LITEN FORSKJELL:", dist)
            break
        else:
            score += 1
            prevDist = stone[0]

    return winner, score

def getPositions(image,points):
    """Return positions and points of stones in image."""

    # Generate mask for each color 
    redMask = colorTresh(image,int(redHsv[0,0,0]))
    yellowMask = colorTresh(image,int(yellowHsv[0,0,0]))
    outerMask = colorTresh(image,int(outerHsv[0,0,0]))
    innerMask = colorTresh(image,int(innerHsv[0,0,0]))

    showIm("red",redMask,0.5)
    showIm("yellow",yellowMask,0.5)
    showIm("outer",outerMask,0.5)

    # Find circles in each mask
    redCircles = detectCircle(redMask,5,stoneR-radMarg,stoneR+radMarg)
    yellowCircles = detectCircle(yellowMask,5,stoneR-radMarg,stoneR+radMarg)
    outerCircle = detectCircle(outerMask,5,outerR-outerMarg,outerR+outerMarg)
    innerCircle = detectCircle(innerMask,5,innerR-innerMarg,innerR+innerMarg)

    # Increase radius to the outer edge of the stone
    if redCircles is not None:
        changeRadius(redCircles,1.332)
    if yellowCircles is not None:
        changeRadius(yellowCircles,1.332)


    # Add data to position dict to send to website
    positions = {}
    centerX = outerCircle[0,0]
    centerY = outerCircle[0,1]
    positions["center"] = { "x" : str(outerCircle[0,0]),
                           "y" : str(outerCircle[0,1]),
                           "rad" : str(outerCircle[0,2])}
    positions["red"] = []
    if redCircles is not None:
        for c in redCircles:
            x = c[0]-centerX
            y = c[1]-centerY
            rad = c[2]

            stone = {"x" : str(x),"y": str(y), "rad" : str(rad), "color" : "red"}
            positions["red"].append(stone)

    positions["yellow"] = []
    if yellowCircles is not None:
        for c in yellowCircles:
            x = c[0]-centerX
            y = c[1]-centerY
            rad = c[2]

            stone = {"x" : str(x),"y": str(y), "rad" : str(rad), "color" : "yellow"}
            positions["yellow"].append(stone)


    # Calculates points to be sent to website
    if points:
        winner, score = calcPoints(redCircles,yellowCircles,outerCircle[0])
        points = {"winner" : winner, "score" : score}
    else:
        points = None

    return positions, points


def main(image):
    redMask = colorTresh(image,int(redHsv[0,0,0]))
    yellowMask = colorTresh(image,int(yellowHsv[0,0,0]))
    outerMask = colorTresh(image,int(outerHsv[0,0,0]))
    innerMask = colorTresh(image,int(innerHsv[0,0,0]))

    redCircles = detectCircle(redMask,5,stoneR-radMarg,stoneR+radMarg)
    yellowCircles = detectCircle(yellowMask,5,stoneR-radMarg,stoneR+radMarg)
    outerCircle = detectCircle(outerMask,5,outerR-outerMarg,outerR+outerMarg)
    innerCircle = detectCircle(innerMask,5,innerR-innerMarg,innerR+innerMarg)

    if redCircles is not None:
        changeRadius(redCircles,1.332)
    if yellowCircles is not None:
        changeRadius(yellowCircles,1.332)


    winner, score = calcPoints(redCircles,yellowCircles,outerCircle[0])
    print(winner,score)


    output = drawCircles(image,(255, 255, 0),redCircles)
    output = drawCircles(output,(13, 255, 37),yellowCircles)
    output = drawCircles(output,(166,0,255),outerCircle)
    output = drawCircles(output,(0,255,100),innerCircle)

    showIm("out",output,0.5)
    cv2.waitKey(0)


def getCookies():
        # Performs GET-request and returns cookies in response.
        return requests.get(SITE_URL).cookies

def sendData(pos,points):
    cookies = getCookies()
    csrf_token = cookies["csrftoken"]
    headers = {'content-type': 'application/json', "X-CSRFToken": csrf_token}       # Add content-type and csrf-token to headers.

    data = json.dumps({ 'pos': pos, 'points': points})    # Dictionary for holding data to be sent.
    print(data)

    response = requests.post(SITE_URL, data=data, cookies=cookies, headers=headers)  # Send data to server.

    if(response.status_code == 200):
            print("Hurra! Dataen er sendt.")
    else:
            print("Noe gikk galt.")
            print("HTTP-Status: {}\n".format(response.status_code))

def takePicture():
    imNum = random.randint(1,12)
    impath = "vancouver/scaled/"+str(imNum)+".png"
    image = cv2.imread(impath)

    pos, points = getPositions(image,True)
    sendData(pos,points)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image",help="path to imput image")
    args = vars(ap.parse_args())

    if args["image"]  == None:
        takePicture()
    else:
        imPath = args["image"]
        image = cv2.imread(imPath)
        pos, points = getPositions(image,True)
        sendData(pos,points)
        main(image)