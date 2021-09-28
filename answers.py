from db import insert, select_by_keys, fetchall, update
from helpers import string_time


def add_answers(answers, question_id):  # for question
    for answer in answers:
        insert('answers', {
            "answer_text": answer["text"],
            "question_id": question_id,
            "is_right": answer["is_right"]
        })


def add_user_answer(user_id: int, question_id: int, answer_id: str):
    insert('user_answers', {
        "user_id": user_id,
        "question_id": question_id,
        "answers": answer_id,
        "answered": string_time["now"]()
    })


def get_user_answers(user_id: int, keys: dict):
    keys["user_id"] = user_id
    return select_by_keys("user_answers", [
        "id", "user_id", "question_id", "answers", "answered"], keys)


def update_user_answer(answer_id, answer):
    update("user_answers", ("answers", answer), answer_id)


def is_right_answer(answer_id: int) -> bool:
    answer = select_by_keys(
        "answers", ["id", "is_right"], {"id": answer_id})
    return answer["is_right"]
