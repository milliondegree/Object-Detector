import cv2
import numpy as np
from matplotlib import pyplot as plt

kernel1=np.ones((8,8),np.uint8)
kernel2=np.ones((10,10),np.uint8)
name='18'
img=cv2.imread('..\\images\\'+name+'.png',0)
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 201, 35)
dilation = cv2.dilate(th, kernel1, iterations=1)
erosion = cv2.erode(dilation,kernel2,iterations = 1)
laplacian = cv2.Laplacian(erosion, cv2.CV_64F)
sobel_8u = np.uint8(laplacian)
# cv2.imwrite('C:\\Users\\CXH\Desktop\\'+name+'b.png',sobel_8u)
image, contours, hierarchy = cv2.findContours(sobel_8u,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
a=[]
ccc=[]
wocao=np.zeros(img.shape,np.uint8)
for contour in contours :
     length=cv2.arcLength(contour,True)
     if length>4000:
      a.append(length)
      ccc.append(contour)
wocao = cv2.drawContours(wocao, ccc, -1, (255,255,255), 1)
# lines = cv2.HoughLines(wocao,1,np.pi/180,600)
# print lines.__len__()
# for line in lines:
#      for rho,theta in line:
#       aa = np.cos(theta)
#       bb = np.sin(theta)
#       x0 = aa*rho
#       y0 = bb*rho
#       x1 = int(x0 + 1000*(-bb))
#       y1 = int(y0 + 1000*(aa))
#       x2 = int(x0 - 1000*(-bb))
#       y2 = int(y0 - 1000*(aa))
#       cv2.line(wocao,(x1,y1),(x2,y2),(255,255,255),2)
cv2.imwrite('..\\TestImages\\'+name+'c.png',wocao)
plt.imshow(wocao,'gray')
plt.show()