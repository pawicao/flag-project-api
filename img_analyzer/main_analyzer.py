import numpy as np
import cv2
from utils.extra import countries_extra, tribands_details
from PIL import Image


# ---------------
# -- Variables --
# ---------------

# Colors HSV boundaries
red = ((0, 40, 20), (13, 255, 255))
red_second = ((170, 40, 20), (180, 255, 255))
yellow = ((19, 40, 20), (34, 255, 255))
green = ((34, 40, 20), (91, 255, 255))
blue = ((85, 40, 20), (135, 255, 255))
white = ((0, 0, 0), (180, 25, 255))

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


# ---
def new_have_colors_eq(countries):
    total_len = len(countries)
    best_proportion = 1.0
    best_value_index = -1
    values = [2, 3, 4, 5, 6]
    true_occurencies_for_values = [0, 0, 0, 0, 0]
    temp_list = []
    for country in countries:
        result_list = new_has_colors_eq(country, 0.005, values)
        temp_list.append(result_list)
        bool_list = result_list[1]
        for i in range (len(bool_list)):
            if bool_list[i]:
                true_occurencies_for_values[i] += 1
    for i in range (len(values)):
        proportion = true_occurencies_for_values[i]/total_len
        if abs(0.5 - proportion) < abs(0.5 - best_proportion):
            best_proportion = proportion
            best_value_index = i
    result_faulty = []
    result_truthy = []
    for i in range (len(countries)):
        record = temp_list[i]
        booly = record[1]
        if booly[best_value_index]:
            result_truthy.append(record[0])
        else:
            result_faulty.append(record[0])
    question_content = "Does the flag have {} colors?".format(values[best_value_index])
    return (question_content, result_truthy, result_faulty, best_proportion)


def new_has_colors_eq(country, threshold, values):
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
    return_list = []
    for val in values:
        return_list.append(len(counted_colors) == val)
    return (country, return_list)


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


#---
def new_have_dominating_color(countries):
    total_len = len(countries)
    best_proportion = 1.0
    best_value_index = -1
    values = [0.35, 0.55]
    true_occurencies_for_values = [0, 0]
    temp_list = []
    for country in countries:
        result_list = new_has_dominating_color(country, values)
        temp_list.append(result_list)
        bool_list = result_list[1]
        for i in range (len(bool_list)):
            if bool_list[i]:
                true_occurencies_for_values[i] += 1
    for i in range (len(values)):
        proportion = true_occurencies_for_values[i]/total_len
        if abs(0.5 - proportion) < abs(0.5 - best_proportion):
            best_proportion = proportion
            best_value_index = i
    result_faulty = []
    result_truthy = []
    for i in range (len(countries)):
        record = temp_list[i]
        booly = record[1]
        if booly[best_value_index]:
            result_truthy.append(record[0])
        else:
            result_faulty.append(record[0])
    question_content = "Is there a color that covers more than {}% of the total flag surface?".format(round(values[best_value_index]*100,0))
    return (question_content, result_truthy, result_faulty, best_proportion)


def new_has_dominating_color(country, values):
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

    return_list = []
    for val in values:
        return_list.append(number_of_occurrences[0]/my_sum > val)
    return country, return_list


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


# ---
def new_first_shade_question(countries):
    result_faulty = []
    result_truthy = []
    for country in countries:
        result = new_first_shade_question_spec(country)
        if result[1]:
            result_truthy.append(result[0])
        else:
            result_faulty.append(result[0])
    question_content = "Does the flag have any shade of green?"
    return question_content, result_truthy, result_faulty


def new_first_shade_question_spec(country):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(green[0], dtype="uint8")
    upper = np.array(green[1], dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)
    return country, (output != 0).any()


def new_have_shade(countries):
    total_len = len(countries)
    best_proportion = 1.0
    best_value_index = -1
    values = [[red, red_second], [yellow], [white], [blue]]
    true_occurencies_for_values = [0, 0, 0, 0]
    temp_list = []
    for country in countries:
        result_list = new_has_shade(country, values)
        temp_list.append(result_list)
        bool_list = result_list[1]
        for i in range (len(bool_list)):
            if bool_list[i]:
                true_occurencies_for_values[i] += 1
    for i in range (len(values)):
        proportion = true_occurencies_for_values[i]/total_len
        if abs(0.5 - proportion) < abs(0.5 - best_proportion):
            best_proportion = proportion
            best_value_index = i
    result_faulty = []
    result_truthy = []
    for i in range (len(countries)):
        record = temp_list[i]
        booly = record[1]
        if booly[best_value_index]:
            result_truthy.append(record[0])
        else:
            result_faulty.append(record[0])
    question_inner_content = ""
    if best_value_index == 0:
        question_inner_content = "red"
    elif best_value_index == 1:
        question_inner_content = "yellow"
    elif best_value_index == 2:
        question_inner_content = "green"
    elif best_value_index == 3:
        question_inner_content = "white"
    elif best_value_index == 4:
        question_inner_content = "blue"
    else:
        return ("The end.", [], [], 1.0)
    question_content = "Does the flag have any shades of {}?".format(question_inner_content)
    return (question_content, result_truthy, result_faulty, best_proportion)


def new_has_shade(country, values):
    return_list = []
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for i in range(len(values)):
        lower = np.array(values[i][0][0], dtype="uint8")
        upper = np.array(values[i][0][1], dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        if len(values[i]) > 1:
            lower = np.array(values[i][1][0], dtype="uint8")
            upper = np.array(values[i][1][1], dtype="uint8")
            mask2 = cv2.inRange(hsv, lower, upper)
            mask = cv2.bitwise_or(mask, mask2)
        output = cv2.bitwise_and(img, img, mask=mask)
        return_list.append((output != 0).any())
    return (country, return_list)


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


#---
def new_have_greater_ratio(countries):
    total_len = len(countries)
    best_proportion = 1.0
    best_value_index = -1
    values = [[8, 5], [2,1]]
    true_occurencies_for_values = [0, 0]
    temp_list = []
    for country in countries:
        result_list = new_has_greater_ratio(country, values)
        temp_list.append(result_list)
        bool_list = result_list[1]
        for i in range (len(bool_list)):
            if bool_list[i]:
                true_occurencies_for_values[i] += 1
    for i in range (len(values)):
        proportion = true_occurencies_for_values[i]/total_len
        if abs(0.5 - proportion) < abs(0.5 - best_proportion):
            best_proportion = proportion
            best_value_index = i
    result_faulty = []
    result_truthy = []
    for i in range (len(countries)):
        record = temp_list[i]
        booly = record[1]
        if booly[best_value_index]:
            result_truthy.append(record[0])
        else:
            result_faulty.append(record[0])
    question_inner_content = str(values[best_value_index][0]) + ':' + str(values[best_value_index][1])
    question_content = "Is the width/height ratio of the flag greater or equal {}?".format(question_inner_content)
    return (question_content, result_truthy, result_faulty, best_proportion)


def new_has_greater_ratio(country, values):
    path = 'assets/flags/' + country['code'] + '.PNG'
    img = Image.open(path)
    width, height = img.size
    img.close()
    return_list = []
    for val in values:
        width_given = val[0]
        height_given = val[1]
        return_list.append((width / height) >= (width_given / height_given))
    return country, return_list

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


#---
def new_have_triangle(countries):
    result_faulty = []
    result_truthy = []
    for country in countries:
        result = new_has_triangle(country)
        if result[1]:
            result_truthy.append(result[0])
        else:
            result_faulty.append(result[0])
    question_content = "Is there a triangular element on the flag?"
    return question_content, result_truthy, result_faulty, len(result_truthy)/len(countries)


def new_has_triangle(country):
    if country['code'] == "ISR":
        return country, True
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
            return country, True
    return country, False


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


#---
def new_have_shape(countries):
    total_len = len(countries)
    best_proportion = 1.0
    best_value_index = -1
    values = ["has_cross", "has_star", "has_other_symbols", "is_triband"]
    true_occurencies_for_values = [0, 0, 0, 0]
    temp_list = []
    for country in countries:
        result_list = new_has_shape(country, values)
        temp_list.append(result_list)
        bool_list = result_list[1]
        for i in range (len(bool_list)):
            if bool_list[i]:
                true_occurencies_for_values[i] += 1
    for i in range (len(values)):
        proportion = true_occurencies_for_values[i]/total_len
        if abs(0.5 - proportion) < abs(0.5 - best_proportion):
            best_proportion = proportion
            best_value_index = i
    result_faulty = []
    result_truthy = []
    for i in range (len(countries)):
        record = temp_list[i]
        booly = record[1]
        if booly[best_value_index]:
            result_truthy.append(record[0])
        else:
            result_faulty.append(record[0])
    question_content = ""
    if best_value_index == 0:
        question_content = "Are there any crosses on the flag?"
    elif best_value_index == 1:
        question_content = "Are there any stars on the flag?"
    elif best_value_index == 2:
        question_content = "Are there any symbols (except stars and crosses) on the flag?"
    elif best_value_index == 3:
        question_content = "Is the flag a triband?"
    else:
        return "The end.", [], [], 1.0
    return question_content, result_truthy, result_faulty, best_proportion


def new_has_shape(country, values):
    return_list = []
    for val in values:
        return_list.append(countries_extra[country['code']][val])
    return country, return_list


# Function wrapper (extra_params[0] - shape parameter (triband))
def are_vertical_triband(countries, answer, extra_params):
    if answer:
        return list(filter(lambda country: is_vertical_triband(country, extra_params[0]), countries))
    return list(filter(lambda country: not is_vertical_triband(country, extra_params[0]), countries))


# Checks the boolean parameter in the extra triband countries dictionary
def is_vertical_triband(country, shape):
    return tribands_details[country['code']][shape]


#---
def new_are_vertical_triband(countries):
    result_faulty = []
    result_truthy = []
    for country in countries:
        result = new_is_vertical_triband(country)
        if result[1]:
            result_truthy.append(result[0])
        else:
            result_faulty.append(result[0])
    question_content = "Is this flag a vertical triband?"
    return question_content, result_truthy, result_faulty, len(result_truthy)/len(countries)


def new_is_vertical_triband(country):
    code = country['code']
    if code in tribands_details:
        return country, tribands_details[code]["vertical_triband"]
    return country, False
