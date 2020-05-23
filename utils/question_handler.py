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
    3: Question(3, "Does the flag have any shades of red?", have_shade, [red]),
    4: Question(4, "Does the flag have any shades of yellow?", have_shade, [yellow]),
    5: Question(5, "Does the flag have 4 colors?", have_colors_eq, [4, 0.005]),
    6: Question(6, "Is the width/height ratio of the flag greater than 8:5?", have_greater_ratio, [8, 5]),
    7: Question(7, "Is there a cross element on the flag?", have_shape, ["has_cross"]),
    8: Question(8, "Are there any stars on the flag?", have_shape, ["has_star"]),
    9: Question(9, "Is there a triangular element on the flag?", have_triangle, None),
    10: Question(10, "Are there any other symbols on the flag?", have_shape, ["has_other_symbols"])
}


def get_response(countries_arg, question_id, answer):
    return {
        "countries": questions[question_id].function(countries_arg, answer, questions[question_id].extra_params),
        "question": {
            "id": question_id + 1,
            "content": questions[question_id].content
        }
    }
