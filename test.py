import cv2
import numpy as np

# read image
img = cv2.imread("testIMG3.jpg")

# convert img to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# do adaptive threshold on gray image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 6)

# write results to disk
cv2.imwrite("dots_thresh.jpg", thresh)
