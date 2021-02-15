import os, subprocess

def run_command_in_new_gnome_session(command: str):
    os.system(f"gnome-terminal -x {command}")

def get_command_path(command: str) -> str:
    return subprocess.check_output(f"which {command}", shell=True).decode('ascii').rstrip()

def run_text_editor(path: str, text_editor: str):
    command_path = get_command_path(text_editor)
    os.system(f"{command_path} {path}")

def run_nano(path: str):
    run_text_editor(path=path, text_editor='nano')

def run_vi(path: str):
    run_text_editor(path=path, text_editor='vi')

def run_gedit(path: str):
    run_text_editor(path=path, text_editor='gedit')