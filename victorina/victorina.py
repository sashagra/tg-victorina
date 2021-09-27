from questions import get_next_question
from users import get_user_by_id
from buttons import register_btn
from answers import add_user_answer, get_user_answers
from victorina.questioning import question_message


def victorina_messaging(user_id, message=None):
    """Посылает вопрос, принимает и обрабатывает ответ"""
    user = get_user_by_id(user_id)

    # перенаправление незарегистрированных на регистрацию
    if not user or not user["phone"]:
        return "Чтобы участвовать в викторине нужно зарегистрироваться.", register_btn

    if user and not message:  # если не ответ, то есть в сообщении пусто
        question = get_next_question(user_id)
        # задаем вопрос или говорим, что нет вопросов
        return question_message(question)

    else:  # если пришел ответ от участника
        question_id, answer_id = message.split(
            "victorina-answer-")[1].split("_")
        # если вопрос отвечен, то ничего не делаем
        if get_user_answers(user_id, {"question_id": question_id}):
            return "Этот вопрос уже был отвечен", None

        # если до этого не было ответа на этот вопрос, то записываем ответ
        add_user_answer(user_id, question_id, answer_id)
        new_question = get_next_question(user_id)  # и получаем новый вопрос

        return question_message(new_question)
