import numpy as np
import matplotlib.pyplot as plt 
import cv2
from scipy import ndimage
import random
import math


### Define a function for the noise which takes as argument the image and noise probability
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


##Read the image and apply the noirse
img_5 = cv2.imread(r"C:\Users\ASUS\Desktop\Master_SDS\TNI\Mini projet\Pb1\M4.jpg") 
img_5_noised = sp_noise(img_5, 0.006)
plt.imshow(img_5_noised)


### Define the quality function
def rmse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return math.sqrt(err)

rmse(img_5_noised, img_5)

###Loop over the noise and measure the quality at each step
Qualities = []
for i in np.arange(0,0.5,0.05):
    Qualities.append(rmse(sp_noise(img_5, i), img_5))
    print(i)
plt.plot(np.arange(0,0.5,0.05), Qualities )
plt.title('Quality = function(Noise)')
plt.xlabel('Noise density')
plt.ylabel('Quality (RMSE)')


###Loop over the noise probability and check if we correctly apply the process to calculate the sum of money
for j in np.arange(0.005,0.05,0.001):
    img = sp_noise(img_5, j)
   
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    blue_channel, green_channel, red_channel = cv2.split(img)
    threshold_value_blue,img_binary_blue = cv2.threshold(blue_channel,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
     # FFT
    f = np.fft.fft2(img_binary_blue)
    fshift = np.fft.fftshift(f)
    # Apply filter
    keep_fraction = 0.5
    r, c = fshift.shape
    fshift[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
    fshift[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
    # Inverse FFT to denoise image
    fft_inv = np.fft.ifftshift(fshift)
    fft_inv = np.abs(np.fft.ifft2(fft_inv))
    img = fft_inv

    
    img_binary_hue = img
    kernel = np.ones((10, 10),np.uint8)
    img_binary_hue = cv2.erode(img_binary_hue, kernel, iterations=1)
    img_binary_hue = cv2.dilate(img_binary_hue,kernel, iterations = 5)
    threshold_value,img_binary_hue = cv2.threshold(img_binary_hue.astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    img_binary_hue = cv2.bitwise_not(img_binary_hue)
    num_labels, labels_im = cv2.connectedComponents(img_binary_hue.astype(np.uint8))
    plt.imshow(labels_im, cmap="gray")
    
    list_img = []
    for i in range(1, num_labels):
        temp_img = np.where(labels_im == i, 255, 0)
        list_img.append(temp_img)
           
    i=1 
    somme = 0   
    for img in list_img:
        temp = img/np.max(img)
        connectivity = np.ones((3,3))
        resultat = ndimage.morphology.binary_fill_holes(temp,connectivity)
        temp_2 = resultat - temp
        i+=1
        if temp_2.max()==0:
            area = cv2.countNonZero(img)
            print(area)
            if area > 26000 and area < 30000:
                somme += 0.02
            elif area > 39000 and area < 46000:
                somme += 0.2
            elif area > 55000 and area < 60000:
                somme += 2
    print(j)            
    print(somme)        
    
    
    
