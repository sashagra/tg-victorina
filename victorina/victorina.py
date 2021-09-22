from questions import get_question_by_id
from users import get_user_by_id
from buttons import register_btn, inline as inline_btn


def victorina_messenging(user_id, message=None):
    """Посылает вопрос, принимает и обрабатывает ответ"""
    user = get_user_by_id(user_id)
    if not user or not user["phone"]:
        return ("Чтобы участвовать в викторине нужно зарегистрироваться.", register_btn)

    if user and not message:
        # TODO сделать цикл по вопросам
        # TODO сделать разделение на вопросы с одним ответом и с множественным выбором
        question = get_question_by_id(2)
        btn_answers = inline_btn(
            [(answer['answer_text'], f"victorina-otvet-{question['question']['id']}_{answer['id']}") for answer in question["answers"]])

        return (f"Вопрос №{question['question']['id']}.\n{question['question']['question_text']}", btn_answers)
    elif user and message:
        question_id, answer_id = message.split(
            "victorina-otvet-")[1].split("_")
        question = get_question_by_id(int(question_id))
        user_answer = None
        for answer in question["answers"]:
            if answer["id"] == int(answer_id):
                user_answer = answer
                break

        is_right = "верный" if user_answer["is_right"] else "не верный"
        # TODO Запись ответа
        return (f"Ответ принял. Вопрос №{question_id} Этот ответ: {user_answer['answer_text']} {is_right}", None)
    else:
        return ("Чтобы участвовать в викторине нужно зарегистрироваться.", register_btn)
