
#!/usr/bin/env python

from ctypes import *

import sys
import os
from PIL import Image

if sys.platform == 'darwin':
    filename = os.path.join(os.path.dirname(__file__),'lib','darwin-11.4.2-x86_64-i386-64bit','libcolor64.so')
    libcolor64 = CDLL(filename)
elif sys.platform.startswith('linux'):
    filename = os.path.join(os.path.dirname(__file__),'lib','linux2','libcolor64.so')
    libcolor64 = CDLL(filename)
elif sys.platform.startswith('cygwin'):
    filename = os.path.join(os.path.dirname(__file__),'lib','cygwin','libcolor64.so')
    libcolor64 = CDLL(filename)
else:
    filename = os.path.join(os.path.dirname(__file__),'lib','win32','libcolor64.dll')
    libcolor64 = cdll.LoadLibrary(filename)


def fillprototype(f, restype, argtypes):
    f.restype = restype
    f.argtypes = argtypes


def image2bytes(filename):
    try:
        img = Image.open(filename)
        img = img.convert('RGB')
        pixels = img.load()
    except Exception, e:
        print e
        return (None, 0, 0)
    
    if "RGB" != img.mode:
        print "%s is not a RGB image" % filename
        return (None, 0, 0)
        
    nCols, nRows = img.size
    nBytes = nCols * nRows * 3
    pData = (c_ubyte * nBytes)()
    idx = 0
    
    for i in range(nRows):
        for j in range(nCols):
            (r,g,b) = pixels[j,i]
            pData[idx] = r
            pData[idx+1] = g
            pData[idx+2] = b
            idx += 3        
    
    return (pData, nRows, nCols)
    
    
def extractColor64(filename):
    (pData, nRows, nCols) = image2bytes(filename)
    if pData is None:
        print "failed to extract color64 for %s" % filename
        return None

    feature = (c_double * 64)()
    libcolor64.extractColor64(pData, nCols, nRows, feature)
    return feature
    
    
    
fillprototype(libcolor64.extractColor64, None, [POINTER(c_ubyte), c_int, c_int, POINTER(c_double)])


if __name__ == "__main__":
    imfile = os.path.join(os.path.dirname(__file__),'toyset/ImageData/3546946799.jpg')
    feature = extractColor64(imfile)
    print " ".join(["%.8f"%x for x in feature])
    print sum([x**2 for x in feature])  
      
