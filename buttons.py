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


t = 'Привет! 👋'


def add_keyboard(btns: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in btns:
        button = KeyboardButton(btn)
        kb.add(button)
    return kb


register_btn = inline([("Регистрация", "registration")])
victorina_btn = inline([("Начать викторину", "victorina")])
