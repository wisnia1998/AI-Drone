# import the necessary packages
import numpy as np
import argparse
import cv2
import time

cap = cv2.VideoCapture(0) # Set Capture Device, in case of a USB Webcam try 1, or give -1 to get a list of available devices
##set color range
low_blue = np.array([100,10,10])
high_blue = np.array([255,170,170])
x_dif = 0               #diference between x-coordniate of center of circle and center point of picture
y_dif = 0               #diference between y-coordniate of center of circle and center point of picture

while(True):
	# Capture frame-by-frame
        ret, frame = cap.read()
        ##center of frame
        x_center=int(frame.shape[1]/2)      ##center x - coordinate
        y_center=int(frame.shape[0]/2)     ##center y - coordinate
        ##set scale
        scale_percent = 60 # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)           #new dimention of frame
        ## resize image
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        ##first noise reduction
        resized = cv2.medianBlur(resized,5)
        ##transform HSVcollor, treshold blue color
        color_hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)    #convert frame to HSV color
        mask_b = cv2.inRange(color_hsv, low_blue, high_blue)    #get coordinates' array of place witch color in range of low_blue and high_blue
        blue = cv2.bitwise_and(resized,resized, mask = mask_b)  ## put blue color mask on original frame
        # apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
        mask_b = cv2.GaussianBlur(mask_b,(5,5),0);
        mask_b = cv2.medianBlur(mask_b,5)
        
	# Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
        mask_b = cv2.adaptiveThreshold(mask_b,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,3.5)
	
        kernel = np.ones((2,2),np.uint8)
        # mask_b = erosion
        mask_b = cv2.erode(mask_b,kernel,iterations = 1)
	# mask_b = dilation
        mask_b = cv2.dilate(mask_b,kernel,iterations = 1)
        mask_b = cv2.GaussianBlur(mask_b,(5,5),0);
        # detect circles in the image
        circles = cv2.HoughCircles(mask_b, cv2.HOUGH_GRADIENT, 1, 260, param1=30, param2=65, minRadius=0, maxRadius=0)  #return (x,y)-coordinate,r-radius of detected circle

	# ensure at least some circles were found
        if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
		
		# loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                        ##resize x,y coordninate to original size
                        x = int(x*100/scale_percent)
                        y = int(y*100/scale_percent)
                        r = int(r*100/scale_percent)
			# draw the circle in the output image, then draw a rectangle in the image
			# corresponding to the center of the circle
                        cv2.circle(frame, (x,y), r, (0, 255, 0), 4)
                        cv2.rectangle(frame, (x - 5, y - 5), (x + 5,y + 5),(0, 128, 255), -1)
                        
                        x_dif = x_center - x  #The x-shift vector
                        y_dif = y_center - y  #The y-shift vector
                        print ("X offset: ")
                        print (x_dif)
                        print ("Y offset: ")
                        print (y_dif)
                        print ("Radius is: ")
                        print (r)
                        cv2.line(frame, (x,y), (x_center, y_center), (255,100,12), 1)


        
        cv2.circle(frame, (x_center, y_center), 3, (255,100,12), -1)
        ##output = cv2.resize(output, oryginal_dim, interpolation = cv2.INTER_AREA)
        cv2.imshow('m_blue', mask_b)
        cv2.imshow('blue',blue)
        cv2.imshow('frame',frame)
        if cv2.waitKey(27) & 0xFF == ord('q'):
                break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
