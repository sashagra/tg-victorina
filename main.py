import logging
import datetime
from config import BOT_TOKEN, ROOT
from aiogram import Bot, Dispatcher, executor, types
from register import registration, add_user_info
from victorina import victorina_messenging
from db import update
from users import User, get_user_by_id, del_user_by_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

test_users = [504623509, 1124367342, 1659236479]


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    exsisted_user = get_user_by_id(user_id)
    if user_id == ROOT:
        return await message.reply("Тыжадмин")

    if exsisted_user:
        if exsisted_user["login"] == "ADMIN":
            return await message.reply("Уже зарегистрированы как админ. Можете добавить вопросы")

        await message.reply("Уже зарегистрирован. Для начала викторины введи /victorina")
    else:
        await message.reply("Чтобы зарегистрироваться в викторине набери или кликни команду /registration")


@dp.message_handler(commands=['registration', 'admin108'])
async def accept_register(message: types.Message):
    user_id = message.from_user.id
    exsisted_user = get_user_by_id(user_id)
    if exsisted_user:
        if exsisted_user["login"] == "ADMIN":
            return await message.reply("Уже зарегистрированы как админ. Можете добавить вопросы")

        return await message.reply("Уже зарегистрирован. Для начала викторины введи /victorina")

    else:
        if message.text.startswith('/admin108'):
            login = "ADMIN"
        else:
            login = dict(message.from_user).get('username')

        user = User(
            user_id,
            message.from_user.first_name,
            dict(message.from_user).get('last_name'),
            login=login).register_user()
        if user:
            if message.text.startswith('/admin108'):
                return await message.reply("Зарегистрировал администратора. Вы можете добавлять вопросы")

            return await message.reply("Чтобы поучаствовать в викторине также необходимо ввести свой номер телефона\nОтправь свой телефон, набрав сообщение такого вида +375-29-111-11-11\nНеобходимо, чтобы телефон начинался именно с '+375'. То есть в  викторине могут участвовать только жители Беларуси. Телефон нужен для связи с победителями")
        else:
            return await message.reply("Не удалось зарегистрировать. Попробуй снова / registration")


@dp.message_handler(commands=['victorina'])
async def victorina(message: types.Message):
    user_id = message.from_user.id
    exsisted_user = get_user_by_id(user_id)
    answer = victorina_messenging(exsisted_user)
    await message.reply(answer)


@dp.message_handler(commands=['delete'])
async def delete(message: types.Message):
    del_user_by_id(message.from_user.id)
    await message.reply("Вы удалили себя из базы данных. /registration для регистрации")


@dp.message_handler(lambda message: message.text.startswith('+375'))
async def add_info(message: types.Message):
    try:
        # TODO проверить есть ли уже телефон
        update('users', ('phone', message.text), message.from_user.id)
        await message.answer("Добавил телефон. /victorina для начала")
    except:
        await message.answer("Error")


@dp.message_handler(lambda message: message.text.startswith('/otvet'))
async def answer_handler(message: types.Message):
    user_id = message.from_user.id
    exsisted_user = get_user_by_id(user_id)
    answer = victorina_messenging(exsisted_user, message.text)
    await message.answer(answer)


@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    await message.answer("Не понимаю эту команду или сообщение. Пришли что-то понтное. Например, /victorina")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
