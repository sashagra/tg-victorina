from users import User, get_user_by_id


def registration(user_id, first_name, last_name, login):
    exsisted_user = get_user_by_id(user_id)
    if exsisted_user:

        return False
    else:
        User(
            user_id,
            first_name,
            last_name,
            login
        ).register_user()

        return True
