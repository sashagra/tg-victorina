from questions import is_the_questions_tomorrow
from buttons import inline as inline_btn


def test(question):
    return "Test", None


def question_message(question):

    if not question:  # если не осталось неотвеченных вопросов
        return no_questions()

    btns = [(answer['answer_text'],
             f"victorina-answer-{question['question']['id']}_{answer['id']}") for answer in question["answers"]]

    # обработка вопросов с множественным выбором ответа
    m_text = ""
    if question["multiple_answers"]:
        btns.append(("Нет правильного", "victorina-answer-net"))
        m_text = "(Возможно, правильных ответов несколько)"
        # return _multy_answers(question)
    print(
        f"Вопрос {question['question']} множественные ответы {question['multiple_answers']}")
    btn_answers = inline_btn(btns)

    return f"Вопрос №{question['question']['id']}. {m_text}\n{question['question']['question_text']}", btn_answers


def no_questions():
    if is_the_questions_tomorrow():  # проверка, закончилась ли викторина
        reply = "На сегодня вопросов больше нет. Продолжение викторины завтра"
    else:
        reply = "Викторина завершена. Скоро будут результаты"

    return reply, None
