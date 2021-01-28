import numpy as np
import random
import cv2
from matplotlib import pyplot as plt
from skimage.util import invert
from skimage.morphology import skeletonize

img = cv2.imread('texte.bmp',0)
# Invert image
image = invert(img) / np.max(img)
skeleton = skeletonize(image)

# 5 skeletonize
skel_5 = invert(img) / np.max(img)
for i in range(0, 4):
    skel_5 = skeletonize(skel_5)

# Infinite skeletization (1000)
skel_inf = invert(img) / np.max(img)
for i in range(0, 1000):
    skel_inf = skeletonize(skel_inf)

plt.subplot(221)
plt.imshow(img, cmap='gray')
plt.title("Original")
plt.subplot(222)
plt.imshow(invert(skeleton), cmap='gray')
plt.title("1 skeletization")
plt.subplot(223)
plt.imshow(invert(skel_5), cmap='gray')
plt.title("5 skeletization")
plt.subplot(224)
plt.imshow(invert(skel_inf), cmap='gray')
plt.title("infinite skeletization")
plt.show()
