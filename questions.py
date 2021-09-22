from db import insert, select_by_keys, fetchall
from helpers import string_time
from answers import add_answers, get_user_answers


class Question:
    def __init__(self, question, day, answers):
        self.question = question
        self.day = day
        self.answers = answers

    def add(self):
        questions = fetchall('questions', ['id'])
        if questions:
            new_qestion_id = 1 + len(questions)
        else:
            new_qestion_id = 1
        insert('questions', {
            "question_text":    self.question,
            "day":              self.day
        })
        add_answers(self.answers, new_qestion_id)
        return True


def get_next_question(user_id):
    today_questions = select_by_keys(
        'questions',
        ['id', 'question_text', 'day'],
        {'day': string_time["today"]()}
    )
    next_question = None

    for question in today_questions:
        answer = get_user_answers(user_id, {"question_id": question["id"]})
        if not answer:
            next_question = question
            break

    if not next_question:
        return None
    answers = select_by_keys(
        'answers',
        ['id', 'answer_text', 'question_id', 'is_right'],
        {'question_id': next_question["id"]})

    return {
        "question": next_question,
        "answers": answers
    }


def get_question_by_id(question_id):
    question = select_by_keys(
        'questions',
        ['id', 'question_text', 'day'],
        {'id': question_id}
    )
    if not question:
        return None

    answers = select_by_keys(
        'answers',
        ['id', 'answer_text', 'question_id', 'is_right'],
        {'question_id': question_id}
    )
    return {
        "question": question,
        "answers": answers
    }
