from questions import get_question_by_id
from users import get_user_by_id
from buttons import inline as inline_buttons


def victorina_messenging(user_id, message=None):
    """Посылает вопрос, принимает и обрабатывает ответ"""
    user = get_user_by_id(user_id)
    if not user or not user["phone"]:
        return "Чтобы поучаствовать в викторине нужно зарегистрироваться /registration"

    if user and not message:  # задает первый неотвеченый вопрос
        # TODO сделать цикл по вопросам
        question = get_question_by_id(1)
        answers = ""
        for answer in question["answers"]:
            answers += f"- {answer['answer_text']} /otvet{question['question']['id']}_{answer['id']}\n\n"

        return f"Начинаем викторину.\n{question['question']['question_text']}\n\n{answers}"
    elif user and message:
        question_id, answer_id = message.split("/otvet")[1].split("_")
        question = get_question_by_id(int(question_id))
        user_answer = None
        for answer in question["answers"]:
            if answer["id"] == int(answer_id):
                user_answer = answer
                break

        is_right = "верный" if user_answer["is_right"] else "не верный"
        return f"Ответ принял. Вопрос №{question_id} Этот ответ: {user_answer['answer_text']} {is_right}"
    else:
        return "Чтобы участвовать в викторине нужно зарегистрироваться. Команда /registration"
