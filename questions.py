from db import insert, select_by_keys, fetchall
from helpers import string_time


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


def add_answers(answers, question_id):
    for answer in answers:
        insert('answers', {
            "answer_text": answer["text"],
            "question_id": question_id,
            "is_right": answer["is_right"]
        })


def get_today_questions(day):
    data = select_by_keys(
        'questions',
        ['id', 'question_text', 'day'],
        {'day': string_time["today"]()}
    )
    return data


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
        "answers": answers,
        "question": question
    }
