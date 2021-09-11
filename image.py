import cv2
import numpy as np
import os
import random
from PIL import Image
from pixel import putInPool
import webcolors
from progress.bar import ChargingBar

class BigImage:
    path = None
    pixelList = {}

    def __init__(self, path, pixelList):
        self.path = path
        self.pixelList = pixelList

    def build_mosaic(self, size):
        img = Image.open(self.path)
        img = setSize(img, size)
        mosaic = self.__traverse_and_stich(img)
        cv2.imwrite('flipMosaic2.jpg',mosaic)
        return mosaic

    def test(self):
        
        tile = []
        row = []

        for i in range(50):
            row = []
            for j in range(50):
                im = (self.__get_random_pixel('dl')).get_img()
                im_s = cv2.resize(im, dsize=(0, 0), fx=0.1, fy=0.1)
                self.__attach_pixel(im_s,row)
            
            tile.append(row)
        
        
        mosaic = concat_tile(tile)
        cv2.imwrite('save3.jpg',mosaic)
        

    def __traverse_and_stich(self, img):
        est = self.__total_img_estimate(img)
        width, height = img.size
        c = 0
        print(est, width, height)
        tile = []
        row = []

        left = 0
        top = 0
        right = left+5
        bottom = top+5
        
        bar = ChargingBar('Processing', max=est)
        while c != est:
            crop = img.crop((left, top, right, bottom))
            img2 = crop.resize((1, 1))
            color = img2.getpixel((0, 0))
            avgHex = '#{:02x}{:02x}{:02x}'.format(*color)
            pool = putInPool(get_grey_hex(hex_to_rgb(avgHex)))
            pix = self.__get_random_pixel(pool)
            im = pix.get_img()
            im_s = cv2.resize(im, dsize=(0, 0), fx=0.1, fy=0.1)
            self.__attach_pixel(im_s,row)

            if (left + 5) == width:
                left = 0
                right = left+5
                top += 5
                bottom = top+5
                tile.append(row)
                row = []
            else:
                left += 5
                right = left+5

            c+=1
            bar.next()
        
        bar.finish()
        
        mosaic = concat_tile(tile)
        return mosaic
            

    def __total_img_estimate(self, img):
        width, height = img.size
        v = height/5
        h = width/5

        return v*h

    def __attach_pixel(self, img, row):
        row.append(img)
    

    def __get_random_pixel(self, color):
        return random.choice(self.pixelList[color])
    



def setSize(img, size):

    width, height = img.size

    if width != size or height != size:
        img = downOrUpSize(img, size)

    width, height = img.size
    top = 0
    left = 0
    bottom = height
    right = width

    if width % 10 != 0:
        right = width - (width % 10)
    
    if height % 10 != 0:
        bottom = height - (height % 10)
    
    img = img.crop((left, top, right, bottom))

    return img


def downOrUpSize(img, size):
    width, height = img.size
    if width > height:
        basewidth = size
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    else:
        baseheight = size
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    
    return img


def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_grey_hex(rgb):
    avgGrey = (rgb[0]+rgb[1]+rgb[2])/3
    return webcolors.rgb_to_hex((int(round(avgGrey)),int(round(avgGrey)),int(round(avgGrey))))

