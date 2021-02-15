"""
All methods in this package wrap around print, forwarding all arguments, sometimes suppressing all output
"""
import os
import contextlib

BULLET = "\u2022"
RIGHT_ARROW = "\u27f6"

def error(*args, **kwargs):
    print("\033[1;31mError\033[0m: ", end="")
    print(*args, **kwargs)

def note(*args, **kwargs):
    print("[\033[1;33mNOTE\033[0m] ", end="")
    print(*args, **kwargs)

def ok(*args, **kwargs):
    print(*args, **kwargs, end="")
    print(" [\033[1;32mOK\033[0m]")

def x(*args, **kwargs):
    print(*args, **kwargs, end="")
    print(" [\033[1;31mX\033[0m]")

def info(*args, **kwargs):
    print(f" \033[1;36m{RIGHT_ARROW}\033[0m ", end="")
    print(*args, **kwargs)

def bullet(*args, **kwargs):
    print(f"\t{BULLET} ", end="")
    print(*args, **kwargs)

def load_info(msg: str, func, *args, **kwargs):
    info(f"{msg}...", end="", flush=True)
    return exe(func, *args, **kwargs)

def load_bullet(msg: str, func, *args, **kwargs):
    bullet(f"{msg}...", end="", flush=True)
    return exe(func, *args, **kwargs)

def exe(func, *args, **kwargs):
    rv = suppress(func, *args, **kwargs)
    print("\033[1;36mdone\033[0m!")

    return rv

def suppress(func, *args, **kwargs):
    with open(os.devnull, "w") as devnull:
        with contextlib.redirect_stdout(devnull):
            with contextlib.redirect_stderr(devnull):
                rv = func(*args, **kwargs)
    return rv

def abort(status: int, *args, **kwargs):
    error(*args, **kwargs)
    exit(status)

def yes_or_no(*args, **kwargs) -> bool:
    info(*args, **kwargs, end="? [Y/n] ")
    ans = input()
    while ans not in "YyNn":
        bullet("Please enter [Y/n] ")
        ans = input()

    return ans in "Yy"

def options_list(prompt: str, options: list):
    info(f"{prompt}? ")
    descriptions, actions = zip(*options)
    menu = [f"\t{i + 1}. {d}." for (i, d) in enumerate(descriptions)]
    while True:
        try:
            ans = int(input("\n".join(menu) + f"\n \033[1m{RIGHT_ARROW}\033[0m "))
            if not (1 <= ans <= len(options)): raise Exception()
            actions[ans - 1]()
            return 0
        except Exception:
            info(f"Please enter [1-{len(options)}]")


if __name__ == "__main__":
    import time

    response_time_in_seconds = 2
    mock_response = {"id": 5, "name": "Hello pylogtools"}
    mock_api_call = lambda seconds: time.sleep(seconds) or mock_response

    response = load_info(
        f"Imagine fetching data from an API with a response time equal to {response_time_in_seconds} seconds returning {mock_response}", 
        mock_api_call, response_time_in_seconds)

    print()
    note("That was easy")
    bullet("Bullet", "arg1", "arg2", sep="____separator____")
    error("Some error")