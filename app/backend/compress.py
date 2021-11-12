import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
from numpy.linalg import norm
from math import sqrt
from time import time
import os
import logging
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'storage/uploaded/'
DOWNLOAD_FOLDER = 'storage/compressed/'

def svd(A, k, epsilon=1e-3):
    A = np.array(A,dtype=np.float64)
    m = A.shape[0]
    n = A.shape[1]
    X=A.copy()
    if m>=n:
        A = np.dot(A.T,A)
        val = n
        val2 = m
    else:
        A = np.dot(A,A.T)
        val = m
        val2 = n
    now = np.random.rand(val, k)
    now , r = np.linalg.qr(now)
    for i in range(10):
        temp = now
        Z = np.dot(A,now)
        now, R = np.linalg.qr(Z)
        error = ((now-temp) ** 2).sum()
        if error < epsilon:
            break
    sing=np.sqrt(np.abs(np.diag(R)))
    if m<n:
        u=now
        try:
            v=np.dot(np.linalg.inv(np.diag(sing)),np.dot(u.T,X))
        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                return X
    else:
        v=now.T
        try:
            u=np.dot(X,np.dot(v.T,np.linalg.inv(np.diag(sing))))
        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                return X  
    return u, sing, v

def compress_image(img,k):
    logger.info("processing...")
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    try:
        ur,sigr,vr = svd(r,k)
        rr = np.dot(ur[:,:k],np.dot(np.diag(sigr[:k]), vr[:k,:]))
    except ValueError:
        rr = r
    logger.info("compressing...")
    try:
        ug,sigg,vg = svd(g,k)
        rg = np.dot(ug[:,:k],np.dot(np.diag(sigg[:k]), vg[:k,:]))
    except ValueError:
        rg = g
    try:
        ub,sigb,vb = svd(b,k)
        rb = np.dot(ub[:,:k],np.dot(np.diag(sigb[:k]), vb[:k,:]))
    except ValueError:
        rb = b       
    return rr,rg,rb

def arrangeRGB(img,rr,rg,rb):
    logger.info("arranging...")
    result = np.zeros(img.shape)
    result[:,:,0] = rr
    result[:,:,1] = rg
    result[:,:,2] = rb
    for i in range (np.shape(result)[0]):
        for j in range (np.shape(result)[1]):
            for k in range (np.shape(result)[2]):
                if result[i,j,k] < 0:
                    result[i,j,k] = abs(result[i,j,k])
                if result[i,j,k] > 255:
                    result[i,j,k] = 255
    result = result.astype(np.uint8)
    return result

def percentage(img,k):
    m = img.shape[0]
    n = img.shape[1]
    if(m>n):
        return (k*n)//100
    else:
        return (k*m)//100
        
def compress_function(k, image_name):
    # TODO : Support other filetypes
    pth = os.path.abspath(os.getcwd())
    logger.info(pth)
    start = time()
    path = UPLOAD_FOLDER + image_name
    pic = Image.open(path)
    format = pic.format
    mode = pic.mode
    if(mode == 'P'):
        pic = pic.convert('RGBA')
    elif(mode == 'L'):
        pic = pic.convert('RGB')
    elif(mode == 'LA'):
        pic = pic.convert('RGBA')
    img = np.asarray(pic)
    rr,rg,rb = compress_image(img,percentage(img,k))
    result = arrangeRGB(img,rr,rg,rb)
    if(img.shape[2] == 4):
        result[:,:,3] = img[:,:,3]
    image = Image.fromarray(result)
    datas = zip(pic.getdata(), image.getdata())
    diff = sum(abs(i1-i2) for p1,p2 in datas for i1,i2 in zip(p1,p2))
    size = image.size[0] * image.size[1]
    if(mode == 'P'):
        image = image.convert('P')
    elif(mode == 'L'):
        image = image.convert('L')
    elif(mode == 'LA'):
        image = image.convert('LA')
    logger.info("Diff (percentage):", (diff / 255.0 * 100)/size)
    path = DOWNLOAD_FOLDER + "compressed_" + image_name
    image.save(path, format)
    logger.info(f'Time taken to run: {time() - start} seconds')