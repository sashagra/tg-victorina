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

    if today_questions:
        next_question = None

        for question in today_questions:
            answer = is_there_answer(user_id, question["id"])
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
            "answers": answers,
            "multiple_answers": _has_multiple_answers(answers)
        }
    else:
        return None


def is_the_questions_tomorrow():
    tomorrow_questions = select_by_keys(
        'questions',
        ['id', 'question_text', 'day'],
        {'day': string_time["tomorrow"]()}
    )
    return True if tomorrow_questions else False


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
        "answers": answers,
        "multiple_answers": _has_multiple_answers(answers)
    }


def is_there_answer(user_id, question_id):
    question = get_question_by_id(question_id)
    answers = get_user_answers(user_id, {"question_id": question_id})
    if answers:
        if answers["answers"][-2:] == "_0":
            question["multiple_answers"] = False
            answers = answers[:-2]
        answers = answers["answers"].split("_")
    else:
        return False
    # может ответов не быть Нон, может быть отдин ответ с айди, может быть ответ с несколькими айди типа 2_3 а может быть ответ, где последний 2_2_0
    return {
        "multiple_answers": question["multiple_answers"],
        "answers": [int(answer) for answer in answers]
    }


def _has_multiple_answers(answers):
    right_answers = 0
    for answer in answers:
        if answer["is_right"]:
            right_answers += 1

    return True if right_answers > 1 else False
