from GUI import GUI
from HAL import HAL
import numpy as np
import cv2

prev_error = 0

while True:
    # Enter iterative code!
    #get the image and its dimensions
    image = HAL.getImage()
    
    #convert to hsv scale and define thresholds for red color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_thresh = np.array([0, 0, 0])
    upper_thresh = np.array([1, 1, 360])
    
    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    mask = cv2.bitwise_not(mask1)
    
    h, w, d = image.shape
    
    #calculate centre of line detected using moments
    M = cv2.moments(mask)
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(image, (cx, cy), 20, (0, 0, 255), -1)
        err = cx - w/2
        print(err)
        p = float(err)
        d = float(err) - float(prev_error)
        
        GUI.showImage(image)
        
        HAL.motors.sendV(4)
        HAL.motors.sendW(-p/150 - d/150)
        prev_error = float(err)
