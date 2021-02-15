from dataclasses import dataclass


@dataclass
class Config:
    ask_for_sudo_password: bool = False
