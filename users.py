from db import insert, find_one


class User:
    def __init__(self, user_id, first_name, last_name="", login="", phone=""):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.phone = phone

    def is_user_exists(self, id=""):
        return False

    def register_user(self):
        if self.is_user_exists():
            user_info = {
                "id":           self.user_id,
                "firstname":    self.first_name,
                "lastname":     self.last_name,
                "login":        self.login,
                "phone":        self.phone,
            },
            insert('users', user_info)
            return True
        else:
            return False
