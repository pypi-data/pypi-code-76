class Connection:
    def get_session(self):
        return Session()

    def close(self):
        pass


class Session:
    counter = 0
    users = []

    def add_user(self, user):
        Session.counter += 1
        user.id = Session.counter
        self.users.append(user)

    def list_users(self):
        return self.users

    def roll_back(self):
        self.users.clear()

    def close(self):
        pass
