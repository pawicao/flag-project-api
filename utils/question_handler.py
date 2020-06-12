from img_analyzer.main_analyzer import *


class Question:
    def __init__(self, idx, content, function, extra_params):
        self.idx = idx
        self.content = content
        self.function = function
        self.extra_params = extra_params


questions = {
    0: Question(0, "The end.", None, None),
    1: Question(1, "Is it Poland?", find_poland, None),
    2: Question(2, "Does the flag have 3 colors?", have_colors_eq, [3, 0.005]),
    3: Question(3, "Is the flag a triband?", have_shape, ["is_triband"]),
    4: Question(4, "Is this flag a vertical triband", are_vertical_triband, ["vertical_triband"]),
    #4: Question(4, "Does the flag have any shades of yellow?", have_shade, [yellow, None]),
    5: Question(5, "Is the width/height ratio of the flag greater or equal 8:5?", have_greater_ratio, [8, 5]),
    6: Question(6, "Is there a color that covers more than 35% of the total flag surface?", have_dominating_color, [0.35]),
    #6: Question(6, "Does the flag have 4 colors?", have_colors_eq, [4, 0.005]),
    7: Question(7, "Is there a cross element on the flag?", have_shape, ["has_cross"]),
    8: Question(8, "Are there any stars on the flag?", have_shape, ["has_star"]),
    9: Question(9, "Is there a triangular element on the flag?", have_triangle, None),
    10: Question(10, "Are there any other symbols on the flag?", have_shape, ["has_other_symbols"]),
    11: Question(11, "Does the flag have any shades of red?", have_shade, [red, red_second]),
    12: Question(12, "Is there a color that covers more than 55% of the total flag surface?", have_dominating_color, [0.55])
}


def get_response(true_countries, false_countries, answer):
    countries_to_pass = true_countries
    if not answer:
        countries_to_pass = false_countries
    if len(countries_to_pass) == 0:
        return {
            "countries": countries_to_pass,
            "faulty_countries": countries_to_pass,
            "truthy_countries": countries_to_pass,
            "question": {
                "id": 0,
                "content": "The end."
            }
        }
    next_question = get_next_question(countries_to_pass)
    question_id = 555
    if len(countries_to_pass) < 2 or len(countries_to_pass) == len(next_question[2]) or len(countries_to_pass) == len(next_question[1]):
        question_id = 0
    return {
        "countries": countries_to_pass,
        "faulty_countries": next_question[2],
        "truthy_countries": next_question[1],
        "question": {
            "id": question_id,
            "content": next_question[0]
        }
    }


def get_next_question(countries):
    best_proportion = 1.0
    best_question_index = -1
    functions = []
    func_results = []
    functions.append(new_have_colors_eq)
    functions.append(new_have_shade)
    functions.append(new_have_greater_ratio)
    functions.append(new_have_triangle)
    functions.append(new_have_dominating_color)
    functions.append(new_are_vertical_triband)
    functions.append(new_have_shape)
    for i in range (len(functions)):
        func_anchor = functions[i]
        func_results.append(func_anchor(countries))
        proportion = func_results[i][3]
        if abs(0.5 - proportion) < abs(0.5 - best_proportion):
            best_question_index = i
            best_proportion = proportion
    best_question = func_results[best_question_index]
    return (best_question[0], best_question[1], best_question[2])


def get_response_old(countries_arg, question_id, answer):
    return_countries = questions[question_id].function(countries_arg, answer, questions[question_id].extra_params)
    if question_id == max(questions) or len(return_countries) < 2:
        return_id = 0
    else:
        return_id = question_id + 1
    return {
        "countries": return_countries,
        "question": {
            "id": return_id,
            "content": questions[return_id].content
        }
    }