import cv2
import numpy as np

# Morphologic description of the 10 digits
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
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

            width = c_binary.shape[1]
            height = c_binary.shape[0]

            horizontal_segment_width = width
            horizontal_segment_height = 5
            vertical_segment_width = 5
            vertical_segment_height = int(height/2)
            middle_width = int(width/2)
            quarter_height=int(vertical_segment_height/2)
            # A full white square means no number was here
            if(np.count_nonzero(c_binary) > 470):
                digits.append(0)
                continue
            segments = []
            segments.append((0,horizontal_segment_height,middle_width-3,middle_width+3))
            segments.append((quarter_height-3,quarter_height+3, 4,vertical_segment_width+4))                                # Top left
            segments.append((quarter_height-3,quarter_height+3, c_binary.shape[1]-6,c_binary.shape[1]-1))                   # Top right
            segments.append((vertical_segment_height-4,vertical_segment_height+1, middle_width-3,middle_width+3))           # Center
            segments.append((int(2.5*quarter_height)-3,int(2.5*quarter_height)+3, 2,vertical_segment_width+2))              # Bottom left
            segments.append((int(2.5*quarter_height)-3,int(2.5*quarter_height)+3, c_binary.shape[1]-8,c_binary.shape[1]-3)) # Bottom right
            segments.append((c_binary.shape[0]-10,c_binary.shape[0]-4, middle_width-3,middle_width+3))                      # Bottom

            val = []
            for seg in segments:
                cv2.rectangle(c, (seg[2], seg[0]), (seg[3], seg[1]), (0, 255, 0), 1)
                cropped_region = c_binary[seg[0]:seg[1],seg[2]:seg[3]]
                if(np.count_nonzero(cropped_region) > 0.3*cropped_region.shape[0]*cropped_region.shape[1]):
                    val.append(1)
                else:
                    val.append(0)
            val = tuple(val)
            try:
                digits.append(DIGITS_LOOKUP[val])
            except:
                digits.append("-")

        str_hour = ""
        str_hour += str(digits[0]) + str(digits[1]) + ":" + str(digits[2]) + str(digits[3])
        cv2.putText(image,str_hour, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow('frame',image)
        cv2.waitKey(30)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break