# from users import User

# {"id": 504623509, "is_bot": false, "first_name": "Александр",
# "last_name": ".", "username": "tttttws", "language_code": "ru"}

def registration(user):
    # registrated_users = [504623509, 1124367342, 1659236479]
    registrated_users = [1124367342, 1659236479]  # from BD
    if user['id'] not in registrated_users:

        return f"Зарегистрировал.\nИмя: {user['first_name']}\nФамилия: {user['last_name']}\nID: {user['id']}"
    else:
        return "Уже зарегистрирован"


def add_user_info(key, value):
    pass
