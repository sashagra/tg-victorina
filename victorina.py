def victorina_messenging(user, message=None):
    if user and not message:
        return "Начинаем викторину. Первый вопрос: ==вопрос==\nОтвет 1 /otvet1_1\n----\nОтвет 2 /otvet1_2\n----\nОтвет 3 /otvet1_3"
    elif user and message:
        answer = message.split("/otvet")[1].split("_")
        return f"Ответ принял. Вопрос №{answer[0]}, ответ №{answer[1]}"
    else:
        return "Чтобы участвовать в викторине нужно зарегистрироваться. Команда /registration"
