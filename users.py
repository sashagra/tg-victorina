from db import insert, select_by_keys, delete


def get_user_by_id(user_id):
    return select_by_keys(
        'users',
        ["id", "firstname", "lastname", "login", "phone"],
        {'id': str(user_id)})


def del_user_by_id(user_id):
    return delete('users', user_id)


class User:
    def __init__(self, user_id, first_name, last_name, login, phone=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.phone = phone

    def register_user(self):
        user_info = {
            "id":           self.user_id,
            "firstname":    self.first_name,
            "lastname":     self.last_name,
            "login":        self.login,
            "phone":        self.phone
        }

        insert('users', user_info)
        return user_info
