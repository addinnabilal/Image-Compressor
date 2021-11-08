import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from PIL import Image
from time import time

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

def svd(A,k, epsilon=1e-8):
    A = np.array(A, dtype=np.float64)
    m = A.shape[0]
    n = A.shape[1]
    SVD = []
    for i in range(k):
        A1 = A.copy()
        for sig, u, v in SVD[:i]:
            A1 -= sig * np.outer(u, v)
        v = svd1d(A1)
        if m > n:
            u_unnorm = np.dot(A, v)
            sigma = norm(u_unnorm)
            u = u_unnorm / sigma
        else:
            v_unnorm = np.dot(A.T, u)
            sigma = norm(v_unnorm)
            v = v_unnorm / sigma
        SVD.append((sigma, u, v))
    sigs, us, vs = [np.array(x) for x in zip(*SVD)]
    return us.T,sigs, vs

def compress_image(r,g,b,k):
    ur,sigr,vr = svd(r,k)
    ug,sigg,vg = svd(g,k)
    ub,sigb,vb = svd(b,k)
    rr = np.dot(ur[:,:k],np.dot(np.diag(sigr[:k]), vr[:k,:]))
    rg = np.dot(ug[:,:k],np.dot(np.diag(sigg[:k]), vg[:k,:]))
    rb = np.dot(ub[:,:k],np.dot(np.diag(sigb[:k]), vb[:k,:]))
    return rr,rg,rb

def arrange(img,rr,rg,rb):
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

start = time()

img = Image.open(r'C:\Users\airat\OneDrive\Pictures\wp\960ce1b5-ea97-4838-92b9-0feaef724f82.jpg')
img = np.asarray(img)
r = img[:,:,0]
g = img[:,:,1]
b = img[:,:,2]
rr,rg,rb = compress_image(r,g,b,50)
result = arrange(img,rr,rg,rb)
plt.imshow(result)
plt.show()
print(f'Time taken to run: {time() - start} seconds')