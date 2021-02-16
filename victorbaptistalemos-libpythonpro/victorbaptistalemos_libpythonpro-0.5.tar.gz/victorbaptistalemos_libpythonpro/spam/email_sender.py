class EmailSender:
    def send(self, send_from, send_to, send_subject, send_message):
        if '@' not in send_from:
            raise InvalidEmail(f'O e-mail do remetente \'{send_from}\' está inválido.')
        return send_from


class InvalidEmail(Exception):
    pass
