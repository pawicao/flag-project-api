from img_analyzer.main_analyzer import *

questions = {
    1: "Is it Poland?",
    2: "Does the flag have 3 colors?",
    3: "Does the flag have any shades of red?",
    4: "Does the flag have any shades of yellow?",
    5: "Does the flag have 4 colors?",
    6: "Is the width/height ratio of the flag greater than 16:9?",
    7: "Is there a cross element on the flag?",
    8: "Are there any stars on the flag?",
    9: "Is there a triangular element on the flag?",
    10: "Are there any other symbols on the flag?"
}

question_functions = {
    1: find_poland
}


def get_response(countries_arg, question_id, answer):
    return {
        "countries": question_functions[question_id](countries_arg, answer),
        "question": {
            "id": question_id+1,
            "content": questions[question_id]
        }
    }
