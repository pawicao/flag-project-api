# import the necessary packages
import numpy as np
import cv2

# -- Color detection --

# load the image
image = cv2.imread('pol.png')

# define the list of boundaries
#       OPENCV BGR
red = ([20, 20, 108], [233, 233, 251])

# create NumPy arrays from the boundaries
lower = np.array(red[0], dtype="uint8")
upper = np.array(red[1], dtype="uint8")
# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask=mask)
# show the images
cv2.imshow("images", np.hstack([image, output]))
cv2.waitKey(0)
