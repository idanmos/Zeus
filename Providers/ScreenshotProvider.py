#!/usr/bin/env python

import  pyscreenshot as ImageGrab
import io
import base64

def getScreenshot():
    buffer = io.BytesIO()

    imGrab = ImageGrab.grab()
    imGrab.save(buffer, format='PNG')
    imGrab.close()

    bufferImage = buffer.getvalue()
    return bufferImage


def imageToBase64(bufferImage):
    base64Image = base64.b64encode(bufferImage.getvalue())
    return base64Image


def saveBase64ImageLocally(base64Image, fileName):
    imgdata = base64.b64decode(base64Image)
    filename = fileName + ".jpg"
    with open(filename, 'wb') as f:
        f.write(imgdata)


def getBase64Screenshot():
    buffImage = getScreenshot()
    base64Image = imageToBase64(buffImage)
    return base64Image