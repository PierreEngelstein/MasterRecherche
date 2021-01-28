import numpy as np
import random
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from scipy import ndimage, signal
from skimage import filters

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

# Read image and convert to grayscale
img = cv2.imread('Lenna.bmp')
imgred = cv2.split(img)[0]
imggreen = cv2.split(img)[1]
imgblue = cv2.split(img)[2]
print(imggreen)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Compute X and Y gradients

# sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
gradx = signal.convolve2d(img, [[-1, 1], [0, 0]])
# sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
grady = signal.convolve2d(img, [[-1, 0], [1, 0]])
gradient = ndimage.morphological_gradient(img, size=5)
threshold_value,gradient_bin = cv2.threshold(gradient,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
laplacian = ndimage.laplace(img)
# Laplacian with integrated function
laplacian = cv2.Laplacian(img,cv2.CV_64F)
# Laplacian with mask
laplacian_mask = signal.convolve2d(img, [[0, -1, 0], [-1, 4, -1], [0, -1, 0]])

# Roberts filter
robertsx = cv2.filter2D(img, -1, np.array([[1, 0], [0, -1]]))
robertsy = cv2.filter2D(img, -1, np.array([[0, -1], [1, 0]]))
roberts = robertsx + robertsy

# Sobel filter
sobelx = cv2.filter2D(img, -1, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
sobely = cv2.filter2D(img, -1, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
sobel = sobelx + sobely

# Prewitt filter
prewittx = cv2.filter2D(img, -1, np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]]))
prewitty = cv2.filter2D(img, -1, np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]]))
prewitt = prewittx + prewitty

# Canny filter
canny = cv2.Canny(img, 100, 200)

# Gaussian bluring and sobel edge detection
img_blur = cv2.imread('Lenna.bmp')
img_blur = cv2.cvtColor(img_blur, cv2.COLOR_BGR2RGB)
blur = cv2.GaussianBlur(img_blur,(5,5),(0.05)**2, sigmaY=40)
blur = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
sobelx_blur = cv2.filter2D(blur, -1, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
sobely_blur = cv2.filter2D(blur, -1, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
sobel_blur = sobelx_blur + sobely_blur

# Salt & Pepper noise and sobel edge detection
noise_img = sp_noise(img_blur, 0.01)
blur_salt = cv2.cvtColor(noise_img, cv2.COLOR_RGB2GRAY)
sobelx_salt = cv2.filter2D(blur_salt, -1, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
sobely_salt = cv2.filter2D(blur_salt, -1, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
sobel_salt = sobelx_salt + sobely_salt

# Frequency filtering
f = np.fft.fft2(blur_salt)
fshift = np.fft.fftshift(f)
keep_fraction = 0.5
r, c = fshift.shape
fshift[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
fshift[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
fft_inv = np.fft.ifftshift(fshift)
fft_inv = np.abs(np.fft.ifft2(fft_inv))
# Sobel after frequency filtering
sobelx_salt_2 = cv2.filter2D(fft_inv, -1, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
sobely_salt_2 = cv2.filter2D(fft_inv, -1, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
sobel_salt_2 = (sobelx_salt_2 + sobely_salt_2) > filters.threshold_otsu(sobelx_salt_2 + sobely_salt_2)

# Median blur over s&p to filter out the noise
blur_median = cv2.medianBlur(noise_img, 5)
blur_median = cv2.cvtColor(blur_median, cv2.COLOR_RGB2GRAY)
# Sobel after frequency filtering
sobelx_salt_3 = cv2.filter2D(blur_median, -1, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
sobely_salt_3 = cv2.filter2D(blur_median, -1, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
sobel_salt_3 = (sobelx_salt_3 + sobely_salt_3) > filters.threshold_otsu(sobelx_salt_3 + sobely_salt_3)



plt.subplot(551)
plt.imshow(img, cmap=plt.cm.gray)
plt.title("Original")
plt.axis('off')
plt.subplot(552)
plt.imshow(gradx, cmap=plt.cm.gray)
plt.title("Gradient X")
plt.axis('off')
plt.subplot(553)
plt.imshow(grady, cmap=plt.cm.gray)
plt.title("Gradient Y")
plt.axis('off')
plt.subplot(554)
plt.imshow(gradient, cmap=plt.cm.gray)
plt.title("Gradient combination")
plt.axis('off')
plt.subplot(555)
plt.imshow(gradient_bin, cmap=plt.cm.gray)
plt.title("Binary gradient")
plt.axis('off')
plt.subplot(556)
plt.imshow(laplacian, cmap=plt.cm.gray)
plt.title("Laplacien")
plt.axis('off')
plt.subplot(557)
plt.imshow( laplacian_mask, cmap=plt.cm.gray)
plt.title("Laplacien w/ mask")
plt.axis('off')
plt.subplot(558)
plt.imshow( roberts, cmap=plt.cm.gray)
plt.title("Roberts")
plt.axis('off')
plt.subplot(559)
plt.imshow( sobel, cmap=plt.cm.gray)
plt.title("Sobel")
plt.axis('off')
plt.subplot(5,5,10)
plt.imshow( prewitt, cmap=plt.cm.gray)
plt.title("Prewitt")
plt.axis('off')
plt.subplot(5,5,11)
plt.imshow( canny, cmap=plt.cm.gray)
plt.title("Canny")
plt.axis('off')
plt.subplot(5,5,12)
plt.imshow( blur, cmap=plt.cm.gray)
plt.title("Gaussian blur")
plt.axis('off')
plt.subplot(5,5,13)
plt.imshow( sobel_blur, cmap=plt.cm.gray)
plt.title("Sobel blur")
plt.axis('off')
plt.subplot(5,5,14)
plt.imshow( blur_salt, cmap=plt.cm.gray)
plt.title("Salt&pepper")
plt.axis('off')
plt.subplot(5,5,15)
plt.imshow( sobel_salt, cmap=plt.cm.gray)
plt.title("Sobel salt&pepper")
plt.axis('off')
plt.subplot(5,5,16)
plt.imshow( fft_inv, cmap=plt.cm.gray)
plt.title("S&P after frequency filtering")
plt.axis('off')
plt.subplot(5,5,17)
plt.imshow( sobel_salt_2, cmap=plt.cm.gray)
plt.title("Sobel S&P after frequency filtering")
plt.axis('off')
plt.subplot(5,5,18)
plt.imshow( blur_median, cmap=plt.cm.gray)
plt.title("S&P after median blur")
plt.axis('off')
plt.subplot(5,5,19)
plt.imshow( sobel_salt_3, cmap=plt.cm.gray)
plt.title("Sobel S&P after median blur")
plt.axis('off')
plt.subplot(5,5,20)
plt.imshow( imgred, cmap=plt.cm.gray)
plt.title("Image red")
plt.axis('off')
plt.subplot(5,5,21)
plt.imshow( imggreen, cmap=plt.cm.gray)
plt.title("Image green")
plt.axis('off')
plt.subplot(5,5,22)
plt.imshow( imgblue, cmap=plt.cm.gray)
plt.title("Image blue")
plt.axis('off')
plt.show()