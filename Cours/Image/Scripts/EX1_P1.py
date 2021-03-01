import numpy as np
import matplotlib.pyplot as plt 
import cv2
from scipy import ndimage
from os import listdir
from os.path import isfile, join
import pandas as pd

folder_path = r"C:\Users\ASUS\Desktop\Master_SDS\TNI\Mini projet\Pb1"
images_paths = [folder_path+ "\\" +f for f in listdir(folder_path) if isfile(join(folder_path, f))]

dataframe = pd.DataFrame(columns=['File', 'Money (€)'])
for image_path in images_paths:
    ###Read image
    img=cv2.imread(image_path) 
    ### Convert from BGR to HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ### Keep only the blue component
    H_channel = cv2.split(img)[0]
    ### Image threshlding
    threshold_value_h,img_binary_H = cv2.threshold(H_channel,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ### Morphological Transformations: Erosion and dilatation
    img_binary_hue = img_binary_H
    kernel = np.ones((10, 10),np.uint8)
    img_binary_hue = cv2.erode(img_binary_hue, kernel, iterations=1)
    img_binary_hue = cv2.dilate(img_binary_hue,kernel,iterations = 5)
    ### Apply not to the image
    img_binary_hue = cv2.bitwise_not(img_binary_hue)
    ### Extract connected regions
    num_labels, labels_im = cv2.connectedComponents(img_binary_hue)
    ### Save the different regions in a list
    list_img = []
    for i in range(1, num_labels):
        temp_img = np.where(labels_im == i, 255, 0)
        list_img.append(temp_img)
    ### Check if each region is cercular (without a hole)
    ### If it is the case calculate the area of each circle
    ### Based on the area calculate the sum of money
    areas = []
    for i in range(len(list_img)):
        ### For each image we try to fill holes if they exist
        ### By substracting the new image from the original one we can determine if there is a hole or not
        ### If the substraction result is null then there is no hole and it's an image of money
        temp = list_img[i]/np.max(list_img[i])
        connectivity = np.ones((3,3))
        resultat = ndimage.morphology.binary_fill_holes(temp, connectivity)
        temp_2 = resultat - temp
        if temp_2.max()==0:
            area = cv2.countNonZero(list_img[i])
            areas.append(area)
    quantities  = np.array([x for x in np.histogram(areas)[0] if x!=0])
    try:
        money_sum = np.sum(quantities*[0.02, 0.2, 2])
        dataframe = dataframe.append({'File': image_path, 'Money (€)': money_sum }, ignore_index=True)
    except:
        dataframe = dataframe.append({'File': image_path, 'Money (€)': np.nan }, ignore_index=True)
