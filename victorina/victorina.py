from questions import get_next_question, get_question_by_id, is_there_answer
from users import get_user_by_id
from buttons import register_btn, add_keyboard
from answers import add_user_answer, get_user_answers, update_user_answer
from victorina.questioning import question_message, get_info_link


def victorina_messaging(user_id, message=None):
    """Посылает вопрос, принимает и обрабатывает ответ"""

    user = get_user_by_id(user_id)
    # перенаправление незарегистрированных на регистрацию
    if not user or not user["phone"]:
        return "Чтобы участвовать в викторине нужно зарегистрироваться.", register_btn

    if user and not message:  # если не ответ, то есть в сообщении пусто
        question = get_next_question(user_id)
        return question_message(question)

    if message == "справка":
        link = get_info_link(yesterday=True)
        reply = f"Справка по вчерашнему блоку вопросов:\n{link}" if link else "Нет справки по вчерашнему блоку"
        return reply, None

    if message.startswith("Готово В."):
        return _handle_not_right_answer(user_id, message)

        # Отбработка обычного ответа
    return _handle_simple_answer(user_id, message)


def _handle_simple_answer(user_id, message):
    try:
        answer_text = message.split("    ")[1].split("_")
    except IndexError:
        return "Непонятный ответ", None
    try:
        question_id, answer_id = answer_text
    except ValueError:
        return "Непонятный ответ", None

    # если вопрос отвечен, то ничего не делаем
    if is_there_answer(user_id, question_id):
        return "Этот вопрос уже был отвечен", None

    is_answer = False
    question = get_question_by_id(question_id)
    if question["multiple_answers"]:  # если несколько правильных ответов
        old_answer = get_user_answers(user_id, {"question_id": question_id})
        if old_answer:
            if len(question["answers"]) - len(old_answer['answers'][:-1].split("_")) < 2:
                return _handle_not_right_answer(user_id, f"Готово В.{question_id}")

            answer = f"{old_answer['answers']}{answer_id}_"
            update_user_answer(old_answer["id"], answer)
        else:
            answer = str(answer_id) + "_"
            add_user_answer(user_id, question_id, answer)

        new_question = question
        is_answer = answer
    else:
        answer = answer_id
        add_user_answer(user_id, question_id, answer)
        new_question = get_next_question(user_id)

    return question_message(new_question, is_answer)


def _handle_not_right_answer(user_id, message):
    try:
        question_id = int(message.split("Готово В.")[1])
    except ValueError:
        return "Непонятный ответ", None
    if is_there_answer(user_id, question_id):
        return "Этот вопрос уже был отвечен", None

    user_answer = get_user_answers(
        user_id, {"question_id": question_id})
    # Добавляем 0 к ответам получится 1_2_0, но не методом добавление, а нужно поправить
    update_user_answer(user_answer["id"], user_answer["answers"] + "0")
    new_question = get_next_question(
        user_id)  # и получаем новый вопрос
    return question_message(new_question)
