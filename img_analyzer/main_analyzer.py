import numpy as np
import cv2
from utils.extra import countries_extra
from PIL import Image


# ---------------
# -- Variables --
# ---------------

# Colors HSV boundaries
red = ((0, 40, 20), (13, 255, 255))
red_second = ((170, 40, 20), (180, 255, 255))
yellow = ((19, 40, 20), (34, 255, 255))
green = ((34, 40, 20), (85, 255, 255))
blue = ((85, 40, 20), (135, 255, 255))


# ---------------
# -- Functions --
# ---------------

# -- SAMPLE FUNCTION --
# Checks if the country is Poland

# Function wrapper
def find_poland(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: is_poland(country), countries))
    return list(filter(lambda country: not is_poland(country), countries))


# Compares the country code to check if it equals Poland
def is_poland(country):
    return country['code'] == 'POL'


# -- NUMBER OF COLORS --
# Checks if countries have the exact number of colors as given with "extra_param"

# Function wrapper (extra_params[0] - number of colors; extra_params[1] - pixel amount threshold)
def have_colors_eq(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: has_colors_eq(country, extra_params[0], extra_params[1]), countries))
    return list(filter(lambda country: not has_colors_eq(country, extra_params[0], extra_params[1]), countries))


# Counts the amount of pixels of different colors and adds them to length is they're above the threshold
def has_colors_eq(country, value, threshold):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = Image.open(path)
    width, height = img.size
    all_colors = img.getcolors(1000000)
    sorted_colors = sorted(all_colors, reverse=True)
    number_of_occurrences = []
    for i in sorted_colors:
        number_of_occurrences.append(i[0])
    counted_colors = []
    for i in range(len(number_of_occurrences)):
        if number_of_occurrences[i] > (threshold * width * height):
            counted_colors.append(number_of_occurrences[i])
    img.close()
    return len(counted_colors) == value


# -- DOMINATING COLOR --
# Checks if countries has a color which surface is more than "extra_param"% of the flag surface

# Function wrapper (extra_params[0] - percentage)
def have_dominating_color(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: has_dominating_color(country, extra_params[0]), countries))
    return list(filter(lambda country: not has_dominating_color(country, extra_params[0]), countries))


# Counts the amount of pixels of different colors and adds them to length is they're above the threshold
def has_dominating_color(country, percentage):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = Image.open(path)
    all_colors = img.getcolors(1000000)
    sorted_colors = sorted(all_colors, reverse=True)
    number_of_occurrences = []
    for i in sorted_colors:
        number_of_occurrences.append(i[0])

    my_sum = 0
    for i in range(len(number_of_occurrences)):
        my_sum = my_sum + number_of_occurrences[i]
    img.close()
    return number_of_occurrences[0]/my_sum > percentage


# -- COLOR DETECTION --
# Checks if countries flags contain specified colors

# Function wrapper (extra_params[0] - color BGR boundaries)
def have_shade(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: has_shade(country, extra_params[0], extra_params[1]), countries))
    return list(filter(lambda country: not has_shade(country, extra_params[0], extra_params[1]), countries))


# Creates mask within given boundaries and returns True if there are some pixels in an out after bitwise AND operation
def has_shade(country, color_boundaries, color_outer_boundaries):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(color_boundaries[0], dtype="uint8")
    upper = np.array(color_boundaries[1], dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    if color_outer_boundaries is not None:
        lower = np.array(color_outer_boundaries[0], dtype="uint8")
        upper = np.array(color_outer_boundaries[1], dtype="uint8")
        mask2 = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_or(mask, mask2)
    output = cv2.bitwise_and(img, img, mask=mask)
    return (output != 0).any()


# -- ASPECT RATIO --
# Checks if countries flags have aspect ratio greater than given as extra params

# Function wrapper (extra_params[0] - width; extra_params[1] - height)
def have_greater_ratio(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: has_greater_ratio(country, extra_params[0], extra_params[1]), countries))
    return list(filter(lambda country: not has_greater_ratio(country, extra_params[0], extra_params[1]), countries))


# Compares ratios of given width/height vs width/height of the country's flag
def has_greater_ratio(country, width_given, height_given):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = Image.open(path)
    width, height = img.size
    img.close()
    return (width/height) >= (width_given/height_given)


# -- TRIANGLE DETECTION --
# Checks if countries flags contain triangles

# Function wrapper (extra_params[0] - shape parameter)
def have_triangle(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: has_triangle(country), countries))
    return list(filter(lambda country: not has_triangle(country), countries))


# OpenCV triangular shape detection
def has_triangle(country):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    threshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, 0, 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) == 3:
            return True
    return False


# -- OTHER SHAPES DETECTION --
# Checks if countries flags contain given shape

# Function wrapper (extra_params[0] - shape parameter)
def have_shape(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: has_shape(country, extra_params[0]), countries))
    return list(filter(lambda country: not has_shape(country, extra_params[0]), countries))


# Checks the boolean parameter in the extra countries dictionary
def has_shape(country, shape):
    return countries_extra[country['code']][shape]
