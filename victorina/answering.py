from questions import get_question_by_id


def check_answer(question_id, answer_id):
    question = get_question_by_id(int(question_id))

    user_answer = None
    for answer in question["answers"]:
        if answer["id"] == int(answer_id):
            user_answer = answer
            break

    return user_answer["is_right"]
