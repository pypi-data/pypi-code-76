import sys
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from .start_up import APP
from . import contacts as cont
from . import messages as msgs


async def help():
    """
    lists implemented functions
    """
    for key, func in implemented.items():
        if key not in hidden:
            if func.__doc__:
                print(f"{key.rjust(25)}: {func.__doc__.strip()}")
            else:
                print(f"{key.rjust(15)}")


async def exit_repl():
    """
    exits the program
    """
    print("  exiting..")
    sys.exit()


async def quit_repl():
    """
    exits the program
    """
    await exit_repl()


async def version_info():
    """
    displays application information
    """
    print(f"currently running: {APP.name}\nversion: {APP.version} pid: {APP.pid}")


def repl_completer(word_list):
    return WordCompleter(word_list, ignore_case=True, match_middle=True)


def bottom_bar():
    return f'  > {APP.name} > {mode} ' \
           f'{cont.current_contact["alias"]} - ' \
           f'{"U:" + str(msgs.unread)} ' \
           f'{"O:" + str(cont.online)} '


mode = "start_up"
history = InMemoryHistory()
suggest = AutoSuggestFromHistory()

msgs_completer = ["/back", "/exit_chat"]
com_completer = []

prompt_style_chat = Style.from_dict({
    ""                   : "#cccccc",
    "bottom-toolbar"     : "#444444 bg:#222222",
    "bottom-toolbar.text": "#44aa44 bg:#eeeeee",
})

prompt_style_commands = Style.from_dict({
    ""                   : "#cccccc",
    "bottom-toolbar"     : "#444444 bg:#222222",
    "bottom-toolbar.text": "#4444dd bg:#eeeeee",
})

PROMPT = '    your message: '
prompt_session = PromptSession(
    PROMPT,
    history=history,
    bottom_toolbar=bottom_bar,
    style=prompt_style_commands,
)

implemented = {}
hidden = [
    "prompt", "pprint", "not_found", "try_int",
    "repl_completer", "send_msgs", "main",
    'connect_websocket', 'get_message_websocket',
    "chose_action", "init_contacts"
]

