from db import insert, select_by_keys
from helpers import string_time


class Question:
    def __init__(self, question, day):
        self.question = question
        self.day = day

    def add_question(self):
        question_info = {
            "question_text":    self.question,
            "day":              self.day
        }
        insert('questions', question_info)
        return True


def get_today_questions(day):
    data = select_by_keys(
        'questions',
        ['id', 'question_text', 'day'],
        {'day': string_time["today"]()}
    )
    return data


def get_question_by_id(question_id):
    data = select_by_keys(
        'questions',
        ['id', 'question_text', 'day'],
        {'id': question_id}
    )
    return data
