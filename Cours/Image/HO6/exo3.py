import numpy as np
import random
import cv2
from matplotlib import pyplot as plt

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

img = cv2.imread('holmes_nb.bmp',0)
# Apply salt & pepper noise
noise_img = sp_noise(img, 0.2)

# Apply gaussian blur to noisy image
blur_gaussian = cv2.GaussianBlur(noise_img, (5, 5), 0)
# Apply median blur to noisy image
blur_median = cv2.medianBlur(noise_img, 5)

plt.subplot(221)
plt.imshow(img, cmap='gray')
plt.title("Original")
plt.subplot(222)
plt.imshow(noise_img, cmap='gray')
plt.title("Salt & Pepper noise, s²=0.2 ")
plt.subplot(223)
plt.imshow(blur_gaussian, cmap='gray')
plt.title("Gaussian blur")
plt.subplot(224)
plt.imshow(blur_median, cmap='gray')
plt.title("Median blur")
plt.show()

