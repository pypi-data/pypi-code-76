import time
from typing import NoReturn

import pyperclip


def copy(text: str, ttl_secs: int = 10) -> NoReturn:
    pyperclip.copy(text)
    try:
        time.sleep(ttl_secs)
    except KeyboardInterrupt:
        pass
    finally:
        pyperclip.copy("")
