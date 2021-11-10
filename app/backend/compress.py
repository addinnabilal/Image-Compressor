import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from PIL import Image
from time import time
import os
import logging
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'storage/uploaded/'
DOWNLOAD_FOLDER = 'storage/compressed/'

def svd1d(A, epsilon=1e-8):
    m = A.shape[0]
    n = A.shape[1]
    x = [0 for i in range (min(m,n))]
    x[0] = 1
    now = x
    if m > n:
        mtrx = np.dot(A.T, A)
    else:
        mtrx = np.dot(A, A.T)
    while True:
        temp = now
        now = np.dot(mtrx, temp)
        now /= norm(now)
        if abs(np.dot(now, temp)) > 1 - epsilon:
            return now

def svd2(A,k, epsilon=1e-8):
    A = np.array(A, dtype=np.float64)
    m = A.shape[0]
    n = A.shape[1]
    SVD = []
    for i in range(k):
        A1 = A.copy()
        for sing, u, v in SVD[:i]:
            A1 -= sing * np.outer(u, v)
        if m > n:
            v = svd1d(A1)
            u_unnorm = np.dot(A, v)
            sigma = norm(u_unnorm)
            u = u_unnorm / sigma
        else:
            u = svd1d(A1)
            v_unnorm = np.dot(A.T, u)
            sigma = norm(v_unnorm)
            v = v_unnorm / sigma
        SVD.append((sigma, u, v))
    sing, us, vs = [np.array(x) for x in zip(*SVD)]
    return us.T,sing, vs

def svd(A, k, epsilon=1e-8):
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
    temp_vec = np.zeros(shape=(val2,k))
    now = np.random.rand(val, k)
    now , r = np.linalg.qr(now)
    for i in range(250):
        temp = now
        Z = np.dot(A,now)
        now, R = np.linalg.qr(Z)
        error = ((now-temp) ** 2).sum()
        if error < epsilon:
            break
    idx = np.argsort(np.diag(R))[::-1]
    sing=np.diag(R)[idx]
    now = now[:,idx]
    if m<n:
        u=now
        for i in range(k):
            u1 = u[:,i]
            v_unnorm = np.dot(X.T,u1)
            sing[i] = norm(v_unnorm)
            temp_vec[:,i] = v_unnorm/sing[i]
        v = temp_vec.T
    else:
        v=now.T
        for i in range(k):
            v1 = v[i,:]
            u_unnorm = np.dot(X,v1.T)
            sing[i] = norm(u_unnorm)
            temp_vec[:,i] = u_unnorm/sing[i]
        u = temp_vec
    return u, sing, v

def compress_image(img,k):
    logger.info("processing...")
    if(len(img.shape) > 2): #rgb
        r = img[:,:,0]
        g = img[:,:,1]
        b = img[:,:,2]
        ur,sigr,vr = svd(r,k)
        logger.info("compressing...")
        ug,sigg,vg = svd(g,k)
        ub,sigb,vb = svd(b,k)
        rr = np.dot(ur[:,:k],np.dot(np.diag(sigr[:k]), vr[:k,:]))
        rg = np.dot(ug[:,:k],np.dot(np.diag(sigg[:k]), vg[:k,:]))
        rb = np.dot(ub[:,:k],np.dot(np.diag(sigb[:k]), vb[:k,:]))
        return rr,rg,rb
    else: #greyscale
        logger.info("compressing...")
        u,s,v = svd(img,k)
        r = np.dot(u[:,:k],np.dot(np.diag(s[:k]), v[:k,:]))
        return r

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

def arrangegs(img,r):
    logger.info("arranging...")
    result = np.zeros(img.shape)
    result[:,:,0] = r
    for i in range (np.shape(result)[0]):
        for j in range (np.shape(result)[1]):
            if result[i,j] < 0:
                result[i,j] = abs(result[i,j])
            if result[i,j] > 255:
                result[i,j] = 255
    result = result.astype(np.uint8)
    return result

def compress_function(k, image_name):
    # TODO : Support other filetypes
    pth = os.path.abspath(os.getcwd())
    logger.info(pth)
    start = time()
    path = UPLOAD_FOLDER + image_name
    img = Image.open(path)
    img = np.asarray(img)
    if(len(img.shape) > 2):
        rr,rg,rb = compress_image(img,k)
        result = arrangeRGB(img,rr,rg,rb)
    else:
        r = compress_image(img,k)
        result = arrangegs(img,r)
    image = Image.fromarray(result)
    path = DOWNLOAD_FOLDER + "compressed_" + image_name
    image.save(path, 'JPEG')
    logger.info(f'Time taken to run: {time() - start} seconds')
