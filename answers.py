from db import insert, select_by_keys, fetchall
from helpers import string_time


def add_answers(answers, question_id):  # for question
    for answer in answers:
        insert('answers', {
            "answer_text": answer["text"],
            "question_id": question_id,
            "is_right": answer["is_right"]
        })


def add_user_answer(user_id: int, question_id: int, answer_id: int):
    insert('user_answers', {
        "user_id": user_id,
        "question_id": question_id,
        "answer_id": answer_id,
        "answered": string_time["now"]()
    })


def get_user_answers(user_id: int, keys: dict):
    keys["user_id"] = user_id
    return select_by_keys("user_answers", [
        "id", "user_id", "question_id", "answer_id", "answered"], keys)