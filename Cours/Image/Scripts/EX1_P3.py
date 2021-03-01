import numpy as np
import matplotlib.pyplot as plt 
import cv2
from scipy import ndimage
from scipy.fftpack import dct, idct
import math
from skimage.color import rgb2gray


# implement 2D DCT
def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

# implement 2D IDCT
def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')    


# read RGB image and convert to grayscale
img=cv2.imread(r"C:\Users\ASUS\Desktop\Master_SDS\TNI\Mini projet\Pb1\M5.jpg") 
im = rgb2gray(img)
imF = dct2(im)
 

### Apply DCT and IDCT to the image
imF_copy = imF
imF_copy[100:,100:] = 0
imF_copy[100:,:] = 0
imF_copy[:,100:] = 0
im1 = idct2(imF_copy)


# plot original and reconstructed images with matplotlib.pylab
plt.gray()
plt.suptitle('DCT example')
plt.subplot(121), plt.imshow(im), plt.axis('off'), plt.title('original image')
plt.subplot(122), plt.imshow(im1), plt.axis('off'), plt.title('reconstructed image (DCT+IDCT)')
plt.show()

###Mesure the quality or the ration of compression
quality =  np.count_nonzero(imF)/(imF.shape[0]*imF.shape[1])



###Define a function to mesure the PSNR
def PSNR (image1, image2):
    image1 = image1*255
    image2 = image2*255
    return(10*math.log(np.max(image1)**2/np.mean((image1-image2)**2)))
print(PSNR(im, im1))



# Loop over the qunatity compressed 
# Mesure the PSNR and the quality at each step 
# Calculate the some of money at each step
money_sum = []
qualities = []
PSNRs = []
for step in np.arange(10, 1400, 40):
    img=cv2.imread(r"C:\Users\ASUS\Desktop\Master_SDS\TNI\Mini projet\Pb1\M5.jpg") 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H_channel = cv2.split(img)[0]
    im = H_channel
    #plt.imshow(im, cmap='gray')
    imF = dct2(im) 
    imF_copy = imF
    imF_copy[step:,step:] = 0
    imF_copy[step:,:] = 0
    imF_copy[:,step:] = 0
    
    im1 = idct2(imF_copy)    
    qualities.append(np.count_nonzero(imF_copy)/(imF_copy.shape[0]*imF_copy.shape[1]))
    PSNRs.append(PSNR(im/255.0, im1/255.0))
    
    ### Aplly the process implimented on the first part to calculate the sum of money
    im1 = im
    blue_channel = cv2.split(im1)[0]
    threshold_value_blue,img_binary_blue = cv2.threshold(blue_channel,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_binary_hue = img_binary_blue
    kernel = np.ones((10, 10),np.uint8)
    img_binary_hue = cv2.erode(img_binary_hue, kernel, iterations=1)
    img_binary_hue = cv2.dilate(img_binary_hue,kernel,iterations = 5)
    img_binary_hue = cv2.bitwise_not(img_binary_hue)
    num_labels, labels_im = cv2.connectedComponents(img_binary_hue)
    list_img = []
    for i in range(1, num_labels):
        temp_img = np.where(labels_im == i, 255, 0)
        list_img.append(temp_img)
    areas = []
    for i in range(len(list_img)):
        temp = list_img[i]/np.max(list_img[i])
        connectivity = np.ones((3,3))
        resultat = ndimage.morphology.binary_fill_holes(temp, connectivity)
        temp_2 = resultat - temp
        if temp_2.max()==0:
            area = cv2.countNonZero(list_img[i])
            areas.append(area)
    quantities  = np.array([x for x in np.histogram(areas)[0] if x!=0])
    try:
        money_sum.append(np.sum(quantities*[0.02, 0.2, 2]))
    except:
        money_sum.append(0)



### Plot the quality as a PSNR function
plt.plot(qualities, PSNRs)
plt.title('Quality degradation = f(PSNR)')
plt.xlabel('Quality degradation')
plt.ylabel('PSNR')
plt.show()

### Check whether we calculate correctly or wrongly the sum of money
plt.plot(PSNRs, money_sum)
plt.title('money_sum = f(PSNR)')
plt.xlabel('PSNR')
plt.ylabel('Sum of money')
plt.show()



   