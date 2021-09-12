async def registration(message):
    registated_users = [504623509, 1124367342, 1659236479]  # from BD
    if message['from']['id'] not in registated_users:
        print(
            f"Зарегистрировал.\nИмя: {message['from']['first_name']}\nФамилия: {message['from']['last_name']}\nID: {message['from']['id']}")
        await message.reply("Зарегистрировал")
    else:
        await message.reply("Уже зарегистрирован")
