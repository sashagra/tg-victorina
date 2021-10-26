from questions import Question, get_question_by_id
from helpers import string_time, shift_days_formatted
import json


def fill_db(test=False, test_file='test_questions.json'):
    db_file = test_file if test else 'questions_final.json'

    with open(db_file) as f:
        questions = json.load(f)

    if test:
        idx = 0
        day = ""
        question_day = string_time["today"]()
        for q in questions:
            if day == "":
                day = q["day"]
            else:
                if day != q["day"]:
                    idx += 1
                    day = q["day"]

                question_day = shift_days_formatted(idx)
            question = Question(q["question"], question_day, q["answers"])
            question.add()
    else:
        for q in questions:
            question = Question(q["question"], q["day"], q["answers"])
            question.add()
