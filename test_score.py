from answers import user_score_compute
from users import get_all_users

users = get_all_users()
for user in users:
    print(user["firstname"], user_score_compute(user["id"]))
