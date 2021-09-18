import logging
import register
from db import update
from config import BOT_TOKEN, ROOT, ADMIN
from aiogram import Bot, Dispatcher, executor, types
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
        await message.reply("Уже зарегистрирован. Для начала викторины введи /victorina")
    else:
        await message.reply("Чтобы зарегистрироваться в викторине набери или кликни команду /registration")


@dp.message_handler(commands=['registration'])
async def accept_register(message: types.Message):
    """
    Обрабатывает команду регистрации в викторине
    """
    user_id = message.from_user.id
    if user_id == ADMIN or user_id == 'ROOT':  # админам не нужно регистрироваться
        return await message.reply("Вам не нужно регистрироваться, вы - ведущий. У вас есть команды для управления викториной и просмотра статистики /admin108")

    user = register.registration(user_id,
                                 first_name=message.from_user.first_name,
                                 last_name=dict(message.from_user).get(
                                     'last_name'),
                                 login=dict(message.from_user).get('username'))
    # TODO запрос номера телефона
    if user:
        return await message.reply("Чтобы поучаствовать в викторине также необходимо ввести свой номер телефона\nОтправь свой телефон, набрав сообщение такого вида +375-29-111-11-11\nНеобходимо, чтобы телефон начинался именно с '+375'. То есть в  викторине могут участвовать только жители Беларуси. Телефон нужен для связи с победителями")
    else:
        return await message.reply("Уже зарегистрирован в викторине. Для начала введи или кликни команду /victorina")


@dp.message_handler(commands=['admin108', 'stat', 'users'])
async def admin(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN or user_id == ROOT:
        # TODO сделать меню с другими командами
        await message.answer("Меню администратора")
    else:
        await message.answer("Не понимаю эту команду или сообщение. Пришли что-то понятное. Например, /victorina")


@dp.message_handler(commands=['victorina'])
async def victorina(message: types.Message):
    answer = victorina_messenging(message.from_user.id)
    await message.reply(answer)


@dp.message_handler(commands=['delete'])  # TODO удалить функцию при запуске
async def delete(message: types.Message):
    del_user_by_id(message.from_user.id)
    await message.reply("Вы удалили себя из базы данных. /registration для регистрации")


@dp.message_handler(lambda message: message.text.startswith('+375'))
async def add_info(message: types.Message):
    try:
        update('users', ('phone', message.text), message.from_user.id)
        await message.answer(f"Добавил/обновил телефон. Проверь правильность и введи заново или команду /victorina для начала/продолжения викторины\n Твой номер: {message.text}")
    except:
        await message.answer("Error")


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
