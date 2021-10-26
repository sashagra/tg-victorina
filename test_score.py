from answers import user_score_compute
from users import get_all_users

users = get_all_users()
for user in users:
    user_login = f"https://t.me/{user['login']}" if user['login'] else user['login']
    print(user["firstname"], user["lastname"], user_login,
          user["phone"], user_score_compute(user["id"]))
