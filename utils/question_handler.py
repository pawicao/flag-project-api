from img_analyzer.main_analyzer import *
from utils.extra import special_questions


def check_special_questions(countries):
    if len(countries) == 2:
        if check_special_country(countries, ["ECU", "SRB"]):
            return 1
        if check_special_country(countries, ["AZE", "UZB"]):
            return 2
        if check_special_country(countries, ["KWT", "ARE"]):
            return 3
        if check_special_country(countries, ["MLI", "GIN"]):
            return 4
        if check_special_country(countries, ["TCD", "ROU"]):
            return 5
        if check_special_country(countries, ["AUS", "NZL"]):
            return 6
        if check_special_country(countries, ["RUS", "NLD"]):
            return 7
        if check_special_country(countries, ["WSM", "PRK"]):
            return 2
        if check_special_country(countries, ["ISL", "NOR"]):
            return 9
        if check_special_country(countries, ["LBR", "USA"]):
            return 2
        if check_special_country(countries, ["TUN", "TUR"]):
            return 11
        if check_special_country(countries, ["DNK", "GEO"]):
            return 14
        if check_special_country(countries, ["GRL", "IDN"]):
            return 16

    elif len(countries) == 3:
        if check_special_country(countries, ["PRI", "CHL", "PAN"]):
            return 2
    return 0


def check_special_country(countries, codes_list):
    for country in countries:
        exists = False
        for code in codes_list:
            if country["code"] == code:
                exists = True
        if not exists:
            return False
    return True


def get_response(true_countries, false_countries, answer):
    countries_to_pass = true_countries
    if not answer:
        countries_to_pass = false_countries
    special_questions_value = check_special_questions(countries_to_pass)
    if special_questions_value != 0:
        return get_special_question(countries_to_pass, special_questions_value)
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


def get_special_question(countries, idx):
    faulty_countries = []
    question_content = special_questions[idx]["question"]
    truthy_countries = []
    for country in countries:
        country_code = country["code"]
        if special_questions[idx]["countries"][country_code]:
            truthy_countries.append(country)
        else:
            faulty_countries.append(country)
    return {
        "countries": countries,
        "faulty_countries": faulty_countries,
        "truthy_countries": truthy_countries,
        "question": {
            "id": 556,
            "content": question_content
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
    return best_question[0], best_question[1], best_question[2]
