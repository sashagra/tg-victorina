from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButtonPollType


def request_phone(text: str):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text=text, request_contact=True))
    return keyboard


def inline(buttons: list):
    buttons_markup = InlineKeyboardMarkup()
    for button in buttons:
        text, data = button
        buttons_markup.add(InlineKeyboardButton(text, callback_data=data))

    return buttons_markup


register_btn = inline([("Регистрация", "registration")])
victorina_btn = inline([("Начать викторину", "victorina")])
