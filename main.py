import logging
import register
from db import update
import buttons as btn
from config import BOT_TOKEN, ROOT, ADMIN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from victorina.victorina import victorina_messaging
from users import get_user_by_id, del_user_by_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Обрабатывает команды `/start` и `/help`
    """
    existed_user = get_user_by_id(message.from_user.id)
    if existed_user:
        await message.reply("Для начала викторины кликни кнопку ниже", reply_markup=btn.victorina_btn)
    else:
        await message.reply("Добро пожаловать. Для участия в викторине необходимо зарегистрироваться")
        await bot.send_message(message.from_user.id, "Для регистрации кликни кнопку ниже",   reply_markup=btn.register_btn)


@dp.callback_query_handler(lambda c: c.data == 'victorina')
async def victorina(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # message = callback_query.data if callback_query.data.startswith(
    #     "victorina-answer") else None
    reply, reply_markup = victorina_messaging(user_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, reply, reply_markup=reply_markup)


@dp.message_handler(lambda message: message.text.startswith('Ответ ') or message.text.startswith("Готово В."))
async def handle_answers(message: types.Message):
    reply, reply_markup = victorina_messaging(
        message.from_user.id, message.text)
    await message.reply(reply, reply_markup=reply_markup)


@dp.callback_query_handler(lambda c: c.data == 'registration')
async def registration(callback_query: types.CallbackQuery):
    """
    Обрабатывает команду регистрации в викторине
    """
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    user = get_user_by_id(user_id)
    if user and user["phone"]:
        reply, reply_markup = victorina_messaging(user_id)
        return await bot.send_message(user_id, reply, reply_markup=reply_markup)

    register.registration(user_id,
                          first_name=callback_query.from_user.first_name,
                          last_name=dict(callback_query.from_user).get(
                              'last_name'),
                          login=dict(callback_query.from_user).get('username'))

    keyboard = btn.request_phone("Отправить номер телефона ☎️")
    await bot.send_message(user_id, "Чтобы завершить регистрацию нажми кнопку ниже, чтобы мы записали номер твоего "
                                    "телефона. В викторине могут участвовать только жители Беларуси, поэтому нужен "
                                    "белорусский номер телефона", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def get_telephone_number(message: types.Message, state: FSMContext):
    user_telephone_num = message.contact.phone_number
    user_id = message.from_user.id
    if user_telephone_num.startswith('+375') or user_telephone_num.startswith('375'):
        update('users', ('phone', user_telephone_num), user_id)
        await message.reply("Поздравляем! Ты зарегистрировался в викторине.",   reply_markup=btn.ReplyKeyboardRemove())
        reply, reply_markup = victorina_messaging(user_id)
        await bot.send_message(user_id, reply, reply_markup=reply_markup)
    else:
        await message.reply("Ты не можешь участвовать в викторине, потому что номер телефона не начинается с +375. "
                            "Викторина только для участников из Беларуси. Попробуй зарегистрироваться с другого "
                            "телеграм аккаунта")


@dp.message_handler(commands=['delete'])  # TODO удалить функцию при запуске
async def delete(message: types.Message):
    del_user_by_id(message.from_user.id)
    await message.reply("Вы удалили себя из базы данных",   reply_markup=btn.register_btn)


@dp.message_handler()
async def echo(message: types.Message):
    mes = "справка" if message.text.lower() == "справка" else None
    reply, reply_markup = victorina_messaging(message.from_user.id, mes)
    if not mes:
        await message.answer(f"Не понял твое сообщение. Возвращаюсь к викторине",  reply_markup=None)
    await bot.send_message(message.from_user.id, reply,  reply_markup=reply_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
