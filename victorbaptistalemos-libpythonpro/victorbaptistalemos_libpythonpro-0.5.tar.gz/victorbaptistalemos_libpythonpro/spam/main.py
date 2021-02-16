class SpamSender:
    def __init__(self, session, sender):
        self.session = session
        self.sender = sender

    def send(self, send_from, send_subject, send_message):
        for user in self.session.list_users():
            # There is a list of User() inside Session()
            self.sender.send(
                send_from,
                user.email,
                send_subject,
                send_message
            )
