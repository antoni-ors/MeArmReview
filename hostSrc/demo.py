import sys, os
print (sys.version)
import cv2, math
import time
from matplotlib import pyplot as plt
import signal
import numpy as np
import multiprocessing
import threading
from threading import RLock

print(cv2.__file__)

openPoseDir = "/home/yousof/AI/openpose/"
openPoseLib = openPoseDir + "build/python"
sys.path.append(openPoseLib);
from openpose import pyopenpose as op
import openpose

params = dict()
params["model_folder"] = openPoseDir + "models"
params["hand"] = True
params["hand_detector"] = 0

def plotOpenCVImage(img):
    plt.figure(figsize=(10,18))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


def pointsToDegrees(d):
    BaseIdx = 5
    midIdx = 6
    tipIdx = 8
    hand = 0
    if d.handKeypoints[hand].size != 1:
        points = d.handKeypoints[hand][0, :, :].squeeze()
        all_zeros = not np.any(points)
        if not all_zeros:
            points[:, 1] = d.cvOutputData.shape[1] - points[:, 1]
            dy = points[midIdx, 1] - points[BaseIdx, 1]
            dx = points[midIdx, 0] - points[BaseIdx, 0]
            deg1 = math.degrees(math.atan2(dy, dx))
            dy = points[tipIdx, 1] - points[midIdx, 1]
            dx = points[tipIdx, 0] - points[midIdx, 0]
            deg2 = math.degrees(math.atan2(dy, dx))
            print(deg1 - 90, deg2)


def processImage(img):
    global  opWrapper
    datum = op.Datum()
    datum.cvInputData = img
    opWrapper.emplaceAndPop([datum])
    pointsToDegrees(datum)

bufferLock = RLock()
image = None
isNewImage = False
running = True
def readImages():
    global running, image, isNewImage, bufferLock, cam
    cam = cv2.VideoCapture(0)
    cam.set(3 , 640  ) # width         1920
    cam.set(4 , 480  ) # height        1080
    print("cam.isOpened()", cam.isOpened())
    while cam.isOpened() and running:
        ret, img = cam.read()
        if ret:
            bufferLock.acquire()
            isNewImage = True
            image = img.copy()
            bufferLock.release()
        else:
            break
    print("Releasing Camera!")
    cam.release()

imageReaderThread = threading.Thread(target=readImages)


def signal_handler(signal, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)


imageReaderThread.start()

def captureLastFrame():
    global image, isNewImage, bufferLock
    lastFrame = None
    suc = False
    if isNewImage:
        bufferLock.acquire()
        isNewImage = False
        lastFrame = image.copy()
        bufferLock.release()
        suc = True
    #print("captureLastFrame:", suc)
    return suc, lastFrame

while running:
    ret, frame = captureLastFrame()
    if ret:
        processImage(frame)