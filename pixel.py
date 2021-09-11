import cv2
import numpy as np
import webcolors
from matplotlib import pyplot as plt


class Pixel:
    path = None
    avgColor = None
    GreyPool = None
    use = 0

    def __init__(self, path, multiple, avgColor, Grey):
        self.path = path
        self.use = multiple
        if avgColor == None or Grey == None :
            self.__setColor()
        else:
            self.avgColor = avgColor
            self.GreyPool = Grey

    def __repr__(self):
        return self.GreyPool+' '+self.path

    def get_img(self):
        return cv2.imread(self.path)
    
    def __setColor(self):
        image_bgr = cv2.imread(self.path, cv2.IMREAD_COLOR)
        channels = cv2.mean(image_bgr)
        avgColor = webcolors.rgb_to_hex((int(round(channels[2])), int(round(channels[1])), int(round(channels[0]))))
        self.avgColor = avgColor

        avgGrey = (int(round(channels[2])) + int(round(channels[1])) + int(round(channels[0]))) / 3
        avgColor = webcolors.rgb_to_hex((int(round(avgGrey)),int(round(avgGrey)),int(round(avgGrey))))
        self.GreyPool = putInPool(avgColor)


def putInPool(hex):
    value = hToI(hex)

    if value >= hToI('#000000') and value <= hToI('#444444'):
        return 'd'
    elif value > hToI('#444444') and value <= hToI('#888888'):
        return 'dl'
    elif value > hToI('#888888') and value <= hToI('#cccccc'):
        return 'ld'
    else:
        return 'l'


def hToI(hex):
    return int(hex[1:],16)