"""
scintillant.entry_points.py
~~~~~~~~~~~~~~~~~~~~~~

This module contains the entry-point functions for the scintillant module,
that are referenced in setup.py.
"""

from sys import argv, version_info
from os import getcwd, remove, rename, listdir, path
from shutil import move, rmtree
from zipfile import ZipFile

import requests

from scintillant import BOTTLE_SKILL_TEMPLATE_URL
from scintillant import AIOHTTP_SKILL_TEMPLATE_URL
from scintillant import FAST_API_SKILL_TEMPLATE_URL


def main() -> None:
    """Main package entry point.

    Delegates to other functions based on user input.
    """

    try:
        user_cmd = argv[1]
        if user_cmd in ['--bottle', 'bottle']:
            start_bottle_skill(skill_name=safe_list_get(argv, 2, None))
        elif user_cmd in ['--help', '-h', 'help']:
            print_help(safe_list_get(argv, 2, None))
        else:
            RuntimeError(
                'please supply a command for scintillant - e.g. help.')
    except IndexError:
        RuntimeError('please supply a command for scintillant - e.g. help.')
    return None


def print_help(search_for: str = None):
    print("Scintillant -a tool for quickly creating skills adapted to work "
          "with the 'Dialog' service - the central system of the "
          "Lilia chat bot. \n\n"
          "** Commands ** \n"
          "+ bottle - Download the latest skill template based on the "
          "Bottle framework\n"
          ">> snlt bottle")


def start_bottle_skill(skill_name: str = None):
    """Download the latest skill template"""
    skill_name = input("Skill name: ") if not skill_name else skill_name
    skill_dirrectory = input(f"Skill directory ({skill_name}): ")
    if not skill_dirrectory:
        skill_dirrectory = skill_name
    print("Downloading project template...")

    r = requests.get(BOTTLE_SKILL_TEMPLATE_URL)
    with open('temp.zip', 'wb') as f:
        f.write(r.content)

    with ZipFile('temp.zip', 'r') as repo_zip:
        if skill_dirrectory == '.':
            repo_zip.extractall()
        else:
            repo_zip.extractall('.')

    remove('temp.zip')
    if not skill_dirrectory == '.':
        rename('bottle-skill-template-develop', skill_dirrectory)
    else:
        source = './bottle-skill-template-develop'
        files = listdir(source)
        for file in files:
            move(source + f'/{file}', getcwd())
        rmtree('./bottle-skill-template-develop')

    if not version_info < (3, 9):
        print("Language version below the required by the template")





def start_aiohttp_skill(skill_name: str = None):
    """Download the latest skill template"""
    skill_name = input("Skill name: ") if not skill_name else skill_name
    print("Downloading project template...")
    Repo.clone_from(AIOHTTP_SKILL_TEMPLATE_URL, getcwd() + f'/{skill_name}')


def start_fast_api_skill(skill_name: str = None):
    """Download the latest skill template"""
    skill_name = input("Skill name: ") if not skill_name else skill_name
    print("Downloading project template...")
    Repo.clone_from(FAST_API_SKILL_TEMPLATE_URL, getcwd() + f'/{skill_name}')


def safe_list_get(lst, idx, default):
    """Get list item, otherwise return standard value"""
    try:
        return lst[idx]
    except IndexError:
        return default
