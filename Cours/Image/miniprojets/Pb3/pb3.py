import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import imutils

def rotate_image(image, angle, scale=1.0):
    '''
    Rotates and scales image by angle and scale
    '''
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, scale)
    print(rot_mat)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def findPointsOfInterest(image):
    '''
    Returns the eclipse around the contours of image
    '''
    contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(big_contour)
    # (x_center_orig,y_center_orig),(major_axis_orig,minor_axis_orig),angle_orig = ellipse_orig
    return ellipse

def findExtremePoints(image):
    '''
    Finds the 4 extreme points of an image. Returns left, right, top, bottom as tuples
    '''
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    return extLeft, extRight, extTop, extBot

img_orig = cv2.imread('Capture586_export001_r.JPG', 0)
img_tomodif = cv2.split(cv2.imread('Picture 538.jpg'))[1]
# Resize and rotate to get same base position
img_tomodif = cv2.resize(img_tomodif, (img_orig.shape[0],img_orig.shape[1]), interpolation = cv2.INTER_AREA)
img_tomodif = cv2.rotate(img_tomodif, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Get binary images
threshold_value_blue,img_tomodif_binary = cv2.threshold(img_tomodif,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
img_tomodif_binary = cv2.bitwise_not(img_tomodif_binary)
threshold_value_blue,img_orig_binary = cv2.threshold(img_orig,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
img_orig_binary = cv2.bitwise_not(img_orig_binary)

# Find elipse around image to modify
(xc,yc),(d1,d2),angle = findPointsOfInterest(img_tomodif_binary)
# Find elipse around reference image
(x_center_orig,y_center_orig),(major_axis_orig,minor_axis_orig),angle_orig = findPointsOfInterest(img_orig_binary)

# Rotation-Translation-Scale to apply
delta_angle = angle_orig-angle
delta_x = x_center_orig - xc
delta_y = y_center_orig - yc
M = np.float32([[1, 0, delta_x], [0, 1, delta_y]])
# Rotate image and binary image
img_tomodif_binary = rotate_image(img_tomodif_binary, math.radians(delta_angle))
img_tomodif = rotate_image(img_tomodif, math.radians(delta_angle))
# Translate image and binary image
img_tomodif_binary = cv2.warpAffine(img_tomodif_binary,M,img_tomodif_binary.shape[1::-1], flags=cv2.INTER_LINEAR)
img_tomodif = cv2.warpAffine(img_tomodif,M,img_tomodif.shape[1::-1], flags=cv2.INTER_LINEAR)

# Find extreme points of image_tomodify
extLeft, extRight, extTop, extBot = findExtremePoints(img_tomodif_binary)
# Find extreme points of reference image
extLeft_orig, extRight_orig, extTop_orig, extBot_orig = findExtremePoints(img_orig_binary)

width_orig = extBot_orig[1]-extTop_orig[1]
width_tomodif = extBot[1]-extTop[1]
scale = (width_tomodif-width_orig)/img_tomodif_binary.shape[0]

# Scale image to correct value (using rotate with scale parameter and null angle)
img_tomodif = rotate_image(img_tomodif, 0, 1-scale)
img_tomodif_binary = rotate_image(img_tomodif_binary, 0, 1-scale)

# Get result as percentage of difference
img_diff = img_orig_binary - img_tomodif_binary
result = np.count_nonzero(img_diff) / np.count_nonzero(img_orig_binary)

plt.subplot(141)
plt.imshow(cv2.imread('Picture 538.jpg'))
plt.title("Initial")
plt.subplot(142)
plt.imshow(img_tomodif, cmap='gray')
plt.title("Initial - Gray - transformed")
plt.subplot(143)
plt.imshow(img_orig, cmap='gray')
plt.title("Reference - Gray")
plt.subplot(144)
plt.imshow(img_diff, cmap='gray')
plt.title("Difference : " + str(result))
plt.show()