from questions import Question, get_question_by_id
from helpers import string_time
import json


def final_db():
    with open('questions_final.json') as f:
        questions = json.load(f)

    for q in questions:
        print(q["day"])
        question = Question(q["question"], q["day"], q["answers"])
        question.add()


def test_db():
    with open('questions_final.json') as f:
        questions = json.load(f)

    idx = 0
    day = string_time["today"]()
    for q in questions:
        if idx > 4:
            day = string_time["tomorrow"]()
        question = Question(q["question"], day, q["answers"])
        question.add()
        idx += 1


test_db()
# final_db()
