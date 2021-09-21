import logging
import register
from db import update
import buttons as btn
from config import BOT_TOKEN, ROOT, ADMIN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from victorina.victorina import victorina_messenging
from users import User, get_user_by_id, del_user_by_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Обрабатывает команды `/start` и `/help`
    """
    exsisted_user = get_user_by_id(message.from_user.id)
    if exsisted_user:
        await message.reply("Для начала викторины кликни кнопку ниже", reply_markup=btn.inline(("Викторина", "victorina")))
    else:
        await message.reply("Добро пожаловать. Для участия в викторине ненеобходимо зарегистрироваться")
        await bot.send_message(message.from_user.id, "Для начала кликни кнопку ниже",   reply_markup=btn.inline(("Регистрация", "registration")))


@dp.callback_query_handler(lambda c: c.data.startswith('victorina'))
async def victorina(callback_query: types.CallbackQuery):
    answer = victorina_messenging(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, answer)


@dp.callback_query_handler(lambda c: c.data == 'registration')
async def reg(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)

    if user_id == ADMIN or user_id == 'ROOT':  # админам не нужно регистрироваться
        return await bot.send_message(user_id, "Вам не нужно регистрироваться, вы - ведущий. У вас есть команды для управления викториной и просмотра статистики /admin108")

    register.registration(user_id,
                          first_name=callback_query.from_user.first_name,
                          last_name=dict(callback_query.from_user).get(
                              'last_name'),
                          login=dict(callback_query.from_user).get('username'))

    keyboard = btn.request_phone("Отправить номер телефона ☎️")
    await bot.send_message(user_id, "Чтобы завершить регистрацию нажми кнопку ниже, чтобы мы записали номер твоего телефона. В викторине могут участвовать только жители Беларуси, поэтому нужен белорусский номер телефона", reply_markup=keyboard)


@dp.message_handler(commands=['registration'])
async def accept_register(message: types.Message):
    """
    Обрабатывает команду регистрации в викторине
    """
    user_id = message.from_user.id
    if user_id == ADMIN or user_id == 'ROOT':  # админам не нужно регистрироваться
        return await message.reply("Вам не нужно регистрироваться, вы - ведущий. У вас есть команды для управления викториной и просмотра статистики /admin108")

    register.registration(user_id,
                          first_name=message.from_user.first_name,
                          last_name=dict(message.from_user).get(
                              'last_name'),
                          login=dict(message.from_user).get('username'))

    keyboard = btn.request_phone("Отправить номер телефона ☎️")
    await message.answer("Чтобы завершить регистрацию нажми кнопку ниже, чтобы мы записали номер твоего телефона. В викторине могут участвовать только жители Беларуси, поэтому нужен белорусский номер телефона", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def get_telephone_number(message: types.Message, state: FSMContext):
    user_telephone_num = message.contact.phone_number
    if user_telephone_num.startswith('+375') or user_telephone_num.startswith('375'):
        update('users', ('phone', user_telephone_num), message.from_user.id)
        await message.reply("Поздравляем! Ты зарегистрировался в викторине.",   reply_markup=btn.ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, "Для начала кликни кнопку ниже",   reply_markup=btn.inline(("Начать викторину", "victorina")))
    else:
        await message.reply("Ты не можешь участвовать в викторине, потому что номер телефона не начинается с +375. Викторина только для участников из Беларуси. Попробуй зарегистрироваться с другого телеграм аккаунта")


@dp.message_handler(commands=['admin108', 'stat', 'users'])
async def admin(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN or user_id == ROOT:
        # TODO сделать меню с другими командами
        await message.answer("Меню администратора")
    else:
        await message.answer("Не понимаю эту команду или сообщение. Пришли что-то понятное. Например, /victorina")


@dp.message_handler(commands=['delete'])  # TODO удалить функцию при запуске
async def delete(message: types.Message):
    del_user_by_id(message.from_user.id)
    await message.reply("Вы удалили себя из базы данных. /registration для регистрации")


@dp.message_handler(lambda message: message.text.startswith('/otvet'))
async def answer_handler(message: types.Message):
    user_id = message.from_user.id
    answer = victorina_messenging(user_id, message.text)
    await message.answer(answer)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Не понимаю эту команду или сообщение. Пришли что-то понятное. Например, /victorina")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
