from GUI import GUI
from HAL import HAL
import numpy as np
import cv2
# Enter sequential code!

prev_error = 0
accum_error = 0

while True:
    # Enter iterative code!
    #get the image and its dimensions
    image = HAL.getImage()
    #convert to hsv scale and define thresholds for red color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_thresh1 = np.array([0, 60, 20])
    upper_thresh1 = np.array([7, 100, 60])
    
    lower_thresh2 = np.array([350, 60, 40])
    upper_thresh2 = np.array([360, 90, 60])
    
    mask1 = cv2.inRange(hsv, lower_thresh1, upper_thresh2)
    mask2 = cv2.inRange(hsv, lower_thresh2, upper_thresh2)
    
    print("Running")
    #apply a mask
    mask = mask1 + mask2
    
    mask = cv2.bitwise_not(mask)
    #mask[0:search_top, 0:w] = 0
    #mask[search_bot:h, 0:w] = 0
    
    h, w, d = image.shape
    search_top = 3 * h / 4
    search_bot = search_top * 20
    
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