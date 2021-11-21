from db import update
from config import BOT_TOKEN, ROOT, ADMIN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    print("Message")
    await message.answer(f"Не понял твое сообщение. Возвращаюсь к викторине",  reply_markup=None)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
