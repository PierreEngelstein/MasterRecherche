import cv2
from skimage.util import invert
from skimage.morphology import skeletonize
import numpy as np
from imutils import contours, grab_contours

DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

cap = cv2.VideoCapture('heure2.avi')
# All images in video
while(cap.isOpened()):
    ret, image = cap.read()
    if ret == True:
        ciphers = []
        ciphers.append(image[200:230, 264:283]) # cipher 1
        ciphers.append(image[200:230, 284:305]) # cipher 2
        ciphers.append(image[200:230, 320:343]) # cipher 3
        ciphers.append(image[200:230, 345:366]) # cipher 4
        digits = []
        for c in ciphers:
            c = cv2.split(c)[0]
            threshold_value_blue,c_binary = cv2.threshold(c,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            # cv2.imshow('frame',c_binary)
            # k = cv2.waitKey(500)

            # w = c_binary.shape[1]
            # h = c_binary.shape[0]

            horizontal_segment_width = c_binary.shape[1]
            horizontal_segment_height = 5
            vertical_segment_width = 5
            vertical_segment_height = int(c_binary.shape[0]/2)

            # segments = [
            #     (0, 0, horizontal_segment_width, horizontal_segment_height),
            #     (0, 0, vertical_segment_width, vertical_segment_height),
            #     (horizontal_segment_width-4, 0, vertical_segment_width, vertical_segment_height)
            # ]
            if(np.count_nonzero(c_binary) > 490):
                digits.append(0)
                continue

            segments = []
            segments.append(c_binary[0:horizontal_segment_height, 5:horizontal_segment_width-5])
            segments.append(c_binary[2:vertical_segment_height, 4:vertical_segment_width+4])
            segments.append(c_binary[2:vertical_segment_height, c_binary.shape[1]-6:c_binary.shape[1]-1])
            segments.append(c_binary[c_binary.shape[1]-2:c_binary.shape[1]+3, 5:horizontal_segment_width-7])
            segments.append(c_binary[vertical_segment_height:c_binary.shape[0]-6, 4:vertical_segment_width+4])
            segments.append(c_binary[vertical_segment_height:c_binary.shape[0]-6, c_binary.shape[1]-8:c_binary.shape[1]-3])
            segments.append(c_binary[c_binary.shape[0]-10:c_binary.shape[0]-4, 5:horizontal_segment_width-5])

            val = []
            for seg in segments:
                # cv2.imshow('frame',seg)
                # print(np.count_nonzero(seg), 0.4*seg.shape[0]*seg.shape[1])
                if(np.count_nonzero(seg) > 0.3*seg.shape[0]*seg.shape[1]):
                    val.append(1)
                    # print("1")
                else:
                    val.append(0)
                    # print("0")
                # k = cv2.waitKey(1000)
            val = tuple(val)
            # print(val)
            # print(DIGITS_LOOKUP[val])

            try:
                digits.append(DIGITS_LOOKUP[val])
            except:
                digits.append("-")
            # cv2.imshow('frame',segment_6)

            # k = cv2.waitKey(500)
            # print(np.count_nonzero(c_binary))
            # A full white square means no number was here

                # exit()
            
        str_hour = ""
        str_hour += str(digits[0]) + str(digits[1]) + ":" + str(digits[2]) + str(digits[3])
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,50)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        cv2.putText(image,str_hour, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        cv2.imshow('frame',image)
        cv2.waitKey(300)
        
        '''
        # Crop to interesting content
        box = image[200:230, 260:370]
        # Split RGB into 3 channels, blue seems to be the best
        box = cv2.split(box)[0]
        # Get image as binary
        threshold_value_blue,box_binary = cv2.threshold(box,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        box_binary = cv2.dilate(box_binary, np.ones((2, 2), np.uint8), iterations=1)
        # box_binary = cv2.Canny(box_binary, 50, 200, 255)

        # Detect the different digits
        cnts = cv2.findContours(box_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)
        digitCnts = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >= 5 and (h >= 12 and h <= 40):
                # print(w, h)
                digitCnts.append(c)
                cv2.rectangle(box, (x, y), (x + w, y + h), (0, 255, 0), 3) # Draw, just for testing
        digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

        digits = []
        for c in digitCnts:
            (x, y, w, h) = cv2.boundingRect(c)
            roi = box_binary[y:y+h, x:x+h]

            # Divide the roi in 7 segments parts
            horizontal_segment_width = w
            horizontal_segment_height = h * 0.15
            vertical_segment_width = w * 0.25
            vertical_segment_height = h * 0.5

            segments = [
                (0, 0, horizontal_segment_width, horizontal_segment_height),
                (0, 0, vertical_segment_width, vertical_segment_height),
                (horizontal_segment_width-4, 0, vertical_segment_width, vertical_segment_height)
            ]

            for i in segments:
                cv2.rectangle(box, (x, y),       (x + w, y + h),             (0, 255, 0), 3)
                cv2.rectangle(roi, (i[0], i[1]), (int(i[0] + i[2]), int(i[1] + i[3])), (0, 0, 0), 1)
            # cv2.imshow('frame',roi)
            # k = cv2.waitKey(500)
        if(len(digitCnts) != 3 and len(digitCnts) != 4):
            print(len(digitCnts))
            # exit()
        print("*****")
        cv2.imshow('frame',box)
        '''
        # k = cv2.waitKey(10)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break