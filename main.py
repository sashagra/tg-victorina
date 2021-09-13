import logging
import datetime
from config import BOT_TOKEN, ROOT
from aiogram import Bot, Dispatcher, executor, types
from register import registration, add_user_info
from victorina import victorina_messenging
from users import User, get_user_by_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

test_users = [504623509, 1124367342, 1659236479]


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    if message.from_user.id == ROOT:
        await message.reply("Тыжадмин")
    elif message.from_user.id in test_users:
        await message.reply("Ты участвуешь в викторине. Чтобы получить новый вопрос набери или кликни команду /victorina")
    else:
        await message.reply("Чтобы зарегистрироваться в викторине набери или кликни команду /registration")


@dp.message_handler(commands=['registration'])
async def accept_register(message: types.Message):
    user_id = message.from_user.id
    if get_user_by_id(user_id):
        answer = "Уже зарегистрирован. Для начала викторины введи /victorina"
    else:
        user = User(
            user_id,
            message.from_user.first_name,
            dict(message.from_user).get('last_name'),
            dict(message.from_user).get('login')
        ).register_user()
        if user:
            answer = "Чтобы поучаствовать в викторине также необходимо ввести свой номер телефона\nОтправь свой телефон, набрав сообщение такого вида +375-29-111-11-11\nНеобходимо, чтобы телефон начинался именно с '+375'. То есть в  викторине могут участвовать только жители Беларуси. Телефон нужен для связи с победителями"
        else:
            answer = "Не удалось зарегистрировать. Попробуй снова \registration"
    await message.reply(answer)


@dp.message_handler(commands=['victorina'])
async def victorina(message: types.Message):
    answer = victorina_messenging()
    await message.reply(answer)


@dp.message_handler(commands=['admin108'])
async def admin_register(message: types.Message):
    answer = victorina_messenging()
    await message.reply(answer)


@dp.message_handler(lambda message: message.text.startswith('+375'))
async def add_info(message: types.Message):
    try:
        await message.answer("OK")
    except:
        await message.answer("Error")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Я не понимаю сообщений. Пришли мне команду. Например, /victorina")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
