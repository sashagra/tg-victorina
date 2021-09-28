from questions import is_the_questions_tomorrow, get_user_answers, get_next_question
from answers import update_user_answer
from buttons import add_keyboard, ReplyKeyboardRemove, register_btn, inline as inline_btn

markers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]


def question_message(question, user_answer=None):

    if not question:  # если не осталось неотвеченных вопросов
        return _no_questions()

    btns = [f"Ответ {markers[index]}    {question['question']['id']}_{answer['id']}" for index,
            answer in enumerate(question["answers"])]

    # обработка вопросов с множественным выбором ответа
    answers_text = ""
    if question["multiple_answers"]:
        # не добавлять если еще нет ответов
        if user_answer:
            answers_arr = user_answer[:-1].split("_")
            btns = [btn for btn in btns if btn2answer(
                btn)[1] not in answers_arr]
            btns.append(f"Нет правильного В.{question['question']['id']}")
            return "Можно выбрать еще один ответ или 'Нет правильного'", add_keyboard(btns)
        answers_text += "❗️ Возможно, правильных ответов несколько. За каждый правильный ответ начисляются баллы\n"
    answers_text += "-------\n"
    for index, answer in enumerate(question["answers"]):
        answers_text += f"{markers[index]} {answer['answer_text']}\n\n"

    full_question_text = f"❓ Вопрос №{question['question']['id']}\n{question['question']['question_text']}\n" + answers_text

    return full_question_text, add_keyboard(btns)


def btn2answer(btn_text):
    try:
        answers = btn_text.split("    ")[1].split("_")
    except IndexError:
        return None
    try:
        question_id, answer_id = answers
    except ValueError:
        return None
    return question_id, answer_id


def _no_questions():
    if is_the_questions_tomorrow():  # проверка, закончилась ли викторина
        reply = "На сегодня вопросов больше нет. Продолжение викторины завтра"
    else:
        reply = "Викторина завершена. Скоро будут результаты"

    return reply, ReplyKeyboardRemove()
