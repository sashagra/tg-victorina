from questions import is_the_questions_tomorrow, get_user_answers, get_next_question, get_question_by_id
from answers import update_user_answer
from helpers import string_time, shift_days_formatted, compute_num_of_days
from buttons import add_keyboard, ReplyKeyboardRemove, register_btn, inline as inline_btn

markers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

block_answers = {
    "2021-11-01": "https://telegra.ph/Otvety-i-spravka-po-pervomu-bloku-10-11",
    "2021-11-02": "https://telegra.ph/Vtoroj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-14",
    "2021-11-03": "https://telegra.ph/Vtoroj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-17",
    "2021-11-04": "https://telegra.ph/CHetvyortyj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-17",
    "2021-11-05": "https://telegra.ph/Pyatyj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-17",
    "test": "https://telegra.ph/Eshche-test-09-28"
}

start_day = get_question_by_id(1)["question"]["day"]
test_block_info = [
    "https://telegra.ph/Otvety-i-spravka-po-pervomu-bloku-10-11",
    "https://telegra.ph/Vtoroj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-14",
    "https://telegra.ph/Vtoroj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-17",
    "https://telegra.ph/CHetvyortyj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-17",
    "https://telegra.ph/Pyatyj-blok-viktoriny-Spravka-o-zhizni-SHrily-Prabhupady-10-17"
]


def get_info_link(yesterday=False):
    shift = 0 if not yesterday else 1
    idx = compute_num_of_days(start_day) - shift
    if idx < 0:
        return None
    return test_block_info[idx]


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
            btns.append(f"Готово В.{question['question']['id']}")
            return "Можно выбрать еще один ответ или 'Готово' если больше нет правильных", add_keyboard(btns)
        # answers_text += "❗️ Возможно, правильных ответов несколько. За каждый правильный ответ начисляются баллы\n"
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
    # TODO сделать справку даже если не ответил все вопросы
    try:
        info_link = get_info_link()
        # info_link = block_answers[string_time['today']()]
    except KeyError:
        info_link = block_answers['test']
    return f"{reply}\n{info_link}", ReplyKeyboardRemove()
