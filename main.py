import logging
import datetime
from config import BOT_TOKEN, ROOT
from aiogram import Bot, Dispatcher, executor, types
from register import registration, add_user_info
from victorina import victorina_messenging
from users import User

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
    answer = registration(message.from_user)
    await message.reply(answer)


@dp.message_handler(commands=['victorina'])
async def victorina(message: types.Message):
    answer = victorina_messenging()
    await message.reply(answer)


@dp.message_handler(lambda message: message.text.startswith('del') or message.text.startswith('tel'))
async def add_info(message: types.Message):
    if message.text.startswith('del'):
        answer_message = "Удалил"
    else:
        answer_message = "Позвонил"

    await message.answer(answer_message)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Я не понимаю сообщений. Пришли мне команду. Например, /victorina")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
