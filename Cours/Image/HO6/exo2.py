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

def denoise_sp(image, size_mask):
    # Create mask
    # size_mask=5
    kernel = np.ones((size_mask,size_mask),np.float32)/(size_mask**2)
    # Apply low pass filter to image
    dst = cv2.filter2D(noise_img, -1, kernel)

    # FFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    # Apply filter
    keep_fraction = 0.5
    r, c = fshift.shape
    fshift[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
    fshift[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0

    # Inverse FFT to denoise image
    fft_inv = np.fft.ifftshift(fshift)
    fft_inv = np.abs(np.fft.ifft2(fft_inv))

img = cv2.imread('holmes_nb.bmp',0)
noise_img = sp_noise(img, 0.5)

# fft_inv = denoise_sp(noise_img, 5)

# Create mask
size_mask=5
kernel = np.ones((size_mask,size_mask),np.float32)/(size_mask**2)
# Apply low pass filter to image
dst = cv2.filter2D(noise_img, -1, kernel)

# FFT
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
# Apply filter
keep_fraction = 0.5
r, c = fshift.shape
fshift[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
fshift[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0

# Inverse FFT to denoise image
fft_inv = np.fft.ifftshift(fshift)
fft_inv = np.abs(np.fft.ifft2(fft_inv))


plt.subplot(221)
plt.imshow(img, cmap='gray')
plt.title("Original")
plt.subplot(222)
plt.imshow(noise_img, cmap='gray')
plt.title("Salt & Pepper noise")
plt.subplot(223)
plt.imshow(dst, cmap='gray')
plt.title("Low-pass spatial filter")
plt.subplot(224)
plt.imshow(fft_inv, cmap='gray')
plt.title("Low pass frequency filter")
plt.show()




