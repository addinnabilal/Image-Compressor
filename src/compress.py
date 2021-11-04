import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def compress_image(r,g,b,k):
    sigr,ur,vr = svd(r)
    sigg,ug,vg = svd(g)
    sigb,ub,vb = svd(b)
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
                    result[i,j,k] = 0
                elif result[i,j,k] > 255:
                    result[i,j,k] = 255
    result = result.astype(np.uint8)
    return result

def eigen(A):
    return 0
    
def process_u(A,v, sig):
    u = []
    for i in range(len(v)):
        row = (1/sig[i])*np.dot(A, v[:,i])
        u.append(row)
        
    return np.transpose(np.array(u))


def process_v(A, u, sig):
    v = []
    for i in range(len(u)):
        row = (1/sig[i])*np.dot(A.transpose(), u[:,i])
        v.append(row)

    return np.transpose(np.array(v))

def svd(A):
    m = np.shape(A)[0]
    n = np.shape(A)[1]
    if(m>n):
        AtA = np.dot(np.transpose(A),A)
        sigma,v = eigen(AtA)
        u=process_u(A,v,sigma)
    else:
        AAt = np.dot(A,np.transpose(A))
        sigma,u = eigen(AAt)
        v=process_v(A,u,sigma)
    return sigma,u,v

img = Image.open(r'C:\Users\airat\OneDrive\Pictures\wp\521122.jpg')
img = np.asarray(img)
r = img[:,:,0]
g = img[:,:,1]
b = img[:,:,2]
result = arrange(img,r,g,b)
plt.imshow(result)
plt.show()