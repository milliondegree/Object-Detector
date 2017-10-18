import cv2
import numpy as np

def findcontours(img):
    kernel1 = np.ones((8, 8), np.uint8)
    kernel2 = np.ones((10, 10), np.uint8)
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 201, 35)
    dilation = cv2.dilate(th, kernel1, iterations=1)
    erosion = cv2.erode(dilation, kernel2, iterations=1)
    laplacian = cv2.Laplacian(erosion, cv2.CV_64F)
    sobel_8u = np.uint8(laplacian)
    image, contours, hierarchy = cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    a = []
    ccc = []
    wocao = np.zeros(img.shape, np.uint8)
    for contour in contours:
        length = cv2.arcLength(contour, True)
        if length > 4000:
            a.append(length)
            ccc.append(contour)
    return cv2.drawContours(wocao, ccc, -1, (255, 255, 255), 1)