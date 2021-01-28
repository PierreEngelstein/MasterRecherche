import numpy as np
import random
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('blood.bmp',0)
# Get binary image using OTSU method
threshold_value,img_binary = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

invert = cv2.bitwise_not(img_binary)
contour, hier = cv2.findContours(invert, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contour:
    cv2.drawContours(invert, [cnt], 0, 255, -1)
img2 = cv2.bitwise_not(invert)

# Erosion and dilatation kernel
kernel = np.ones((10, 10),np.uint8)
img2 = cv2.dilate(img2,kernel,iterations = 1)
img2 = cv2.erode(img2, kernel, iterations=1)
img2 = cv2.dilate(img2,kernel,iterations = 1)
img2 = cv2.erode(img2, kernel, iterations=1)

plt.subplot(221)
plt.imshow(img, cmap='gray')
plt.title("Original")
plt.subplot(222)
plt.imshow(img_binary, cmap='gray')
plt.title("Binary conversion with OTSU")
plt.subplot(223)
plt.imshow(img2, cmap='gray')
plt.title("After binary holes filling and noise removal")
plt.show()

plt.subplot(int("44" + str(i)))
