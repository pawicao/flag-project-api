import numpy as np
import cv2
import json
from utils.functions import nope
from PIL import Image


def has_more_colors(countries, answer):
    if answer:
        return list(filter(has_color_eq, countries))
    return list(filter(nope(has_color_eq), countries))


def has_color_eq(country):
    value = 3
    path = 'assets/flags/' + country + '.PNG'
    k = 0.005

    img = Image.open(path)
    width, height = img.size
    all_colors = Image.open(path).getcolors(1000000)
    sorted_colors = sorted(all_colors, reverse=True)
    number_of_occurrences = []
    for i in sorted_colors:
        number_of_occurrences.append(i[0])
    counted_colors = []
    for i in range(len(number_of_occurrences)):
        if number_of_occurrences[i] > (k*width*height):
            counted_colors.append(number_of_occurrences[i])

    return len(counted_colors) == value

# -- Color detection --

# load the image
#image = cv2.imread('pol.png')

# define the list of boundaries
#       OPENCV BGR
#red = ([20, 20, 108], [233, 233, 251])

# create NumPy arrays from the boundaries
#lower = np.array(red[0], dtype="uint8")
#upper = np.array(red[1], dtype="uint8")
# find the colors within the specified boundaries and apply
# the mask
#mask = cv2.inRange(image, lower, upper)
#output = cv2.bitwise_and(image, image, mask=mask)
# show the images
#cv2.imshow("images", np.hstack([image, output]))
#cv2.waitKey(0)


# --
# --
# --
# -- Sample function (returns only Poland if True; removes Poland from list if False) --
def is_poland(country):
    return country['code'] == 'POL'


def find_poland(countries, answer):
    if answer:
        return list(filter(is_poland, countries))
    return list(filter(nope(is_poland), countries))
