# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import json

# Pip
from kcu import request

# Local
from .parse_mode import ParseMode

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: Telegram ------------------------------------------------------------ #

class Telegram:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        token: str,
        chat_id: Optional[str] = None,
        debug: bool = False
    ):
        self.token = token
        self.chat_id = chat_id
        self.debug = debug


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def send(
        self,
        message: str,
        chat_id: Optional[str] = None,
        parse_mode: Optional[ParseMode] = None
    ) -> bool:
        chat_id = chat_id or self.chat_id

        if not chat_id:
            if self.debug:
                print('ERROR: No chat id')

            return False

        res = request.get(
            'https://api.telegram.org/bot{}/sendMessage'.format(self.token),
            params={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': parse_mode.value or 'HTML'
            }
        )

        return res and res.status_code == 200

    @classmethod
    def send_cls(
        cls,
        token: str,
        message: str,
        chat_id: str,
        parse_mode: Optional[ParseMode] = None,
        debug: bool = False
    ) -> bool:
        return cls(token, chat_id, debug).send(message, parse_mode=parse_mode)


# ---------------------------------------------------------------------------------------------------------------------------------------- #