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
    2: Question(2, "Does the flag have any shades of red?", have_shade, [red, red_second]),
    3: Question(3, "Does the flag have any shades of yellow?", have_shade, [yellow, None]),
    4: Question(4, "Does the flag have any shades of blue?", have_shade, [blue, None]),
    5: Question(5, "Does the flag have any shades of green?", have_shade, [green, None]),
    6: Question(6, "Does the flag have 3 colors?", have_colors_eq, [3, 0.005]),
    7: Question(7, "Does the flag have 4 colors?", have_colors_eq, [4, 0.005]),
    8: Question(8, "Is the width/height ratio of the flag greater or equal 8:5?", have_greater_ratio, [8, 5]),
    9: Question(9, "Is there a cross element on the flag?", have_shape, ["has_cross"]),
    10: Question(10, "Are there any stars on the flag?", have_shape, ["has_star"]),
    11: Question(11, "Is there a triangular element on the flag?", have_triangle, None),
    12: Question(12, "Are there any other symbols on the flag?", have_shape, ["has_other_symbols"]),
    13: Question(13, "Is the flag a triband?", have_shape, ["is_triband"]),
    14: Question(14, "Is there a color that covers more than 55% of the total flag surface?", have_dominating_color, [0.55])
}


def get_response(countries_arg, question_id, answer):
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
