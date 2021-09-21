from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButtonPollType


def request_phone(text):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text=text, request_contact=True))
    return keyboard


def test(text):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text=text))
    return keyboard


def inline(*buttons):
    buttons_markup = InlineKeyboardMarkup()
    for button in buttons:
        text, data = button
        buttons_markup.add(InlineKeyboardButton(text, callback_data=data))

    return buttons_markup
