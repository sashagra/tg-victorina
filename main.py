import logging
import datetime
from config import BOT_TOKEN, ROOT
from aiogram import Bot, Dispatcher, executor, types
from register import registration


test_users = [504623509, 1124367342, 1659236479]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    print(message)
    if message['from']['id'] == ROOT:
        await message.reply("Тыжадмин")
    elif message['from']['id'] in test_users:
        await message.reply("Ты участвуешь в викторине. Чтобы получить новый вопрос набери или кликни команду /victorina")
    else:
        await message.reply("Чтобы зарегистрироваться в викторине набери или кликни команду /registration")


@dp.message_handler(commands=['registration'])
async def accept_register(message: types.Message):
    await registration(message)


@dp.message_handler(commands=['ответ'])
async def accept_answer(message: types.Message):

    def parse_answer():
        """
        Answer format: ответ * 1 * Какой-то текст
        """
        arr = message.text.split(" * ")

        print(
            f"Имя: {message['from']['first_name']}\nID: {message['from']['id']}\nЗадача №{arr[1]}\nОтвет: {arr[2]}")

    parse_answer()
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    answer = message.text
    if message['from']['id'] in test_users and answer == "send":
        for user_id in test_users:
            await bot.send_message(user_id, "message.text")
    else:
        await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
