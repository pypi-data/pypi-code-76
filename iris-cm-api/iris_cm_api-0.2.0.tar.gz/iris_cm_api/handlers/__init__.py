from . import (
    add_duty,
    add_to_chat,
    connect,
    delete_messages,
    enable,
    info,
    send_signal,
    set_id,
    transcript,
)

blueprints = [
    add_duty.bot,
    add_to_chat.bot,
    connect.bot,
    delete_messages.bot,
    enable.bot,
    info.bot,
    send_signal.bot,
    set_id.bot,
    transcript.bot,
]
