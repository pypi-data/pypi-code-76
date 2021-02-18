from typing import List
from functools import reduce
from datetime import datetime
from pathlib import Path
import subprocess
import os
import re
import shutil
import webbrowser
import logging
import sh
import json
from donno.config import get_attr


configs = get_attr()
NOTE_FILES = Path(configs['repo']).glob('*.md')
TEMP_FILE = 'newnote.md'
REC_FILE = Path(configs['app_home']) / 'record'
TRASH = Path(configs['app_home']) / 'trash'
DEFAULT_NOTE_LIST = 5
RES_FOLDER = Path('resources')
EXPORT_DIR = 'donno_export'

logger = logging.getLogger('donno')
logger.setLevel(logging.INFO if configs['logging_level'] == 'info'
                else logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)


def update_attachments(notefn: str):
    """ See README.md > Add attachment in a note > Under the hood for
        implementation details
    """
    with open(Path(configs['repo']) / notefn, 'r') as f:
        note = f.read()
    links = re.findall(r'\[.*\]\(\)', note)
    ord_no = 0
    for link in links:
        ord_no += 1
        attfn = link[1:-3]
        attfile = Path.cwd() / attfn
        internal_path = RES_FOLDER / (Path(notefn).stem + 'att' + str(ord_no)
                                      + attfile.suffix)
        if attfile.exists():
            logger.debug(f'copy file from {attfile} to '
                         f'repo_path/{internal_path}')
            sh.cp(attfile, Path(configs['repo']) / internal_path)
            note = note.replace(link, f'[{attfn}]({internal_path})')
        else:
            logger.warn(f'Attachment {attfn} not exists in current folder.\n'
                        f'You can run `don e ...` at the folder'
                        f'where {attfn} exists.')
    with open(Path(configs['repo']) / notefn, 'w') as f:
        f.write(note)


def add_note():
    now = datetime.now()
    created = now.strftime("%Y-%m-%d %H:%M:%S")
    current_nb = configs['default_notebook']
    header = ('Title: \nTags: \n'
              f'Notebook: {current_nb}\n'
              f'Created: {created}\n'
              f'Updated: {created}\n\n------\n\n')
    with open(TEMP_FILE, 'w') as f:
        f.write(header)
    subprocess.run(f'{configs["editor"]} {TEMP_FILE}', shell=True,
                   env={**os.environ, **configs["editor_envs"]})
    # EDITOR_CONF must be put AFTER `os.environ`, for in above syntax,
    # the latter will update the former
    # meanwhile, sh package is not suitable for TUI, so here I use subprocess
    fn = f'note{now.strftime("%y%m%d%H%M%S")}.md'
    logger.debug(f"Save note to {Path(configs['repo']) / fn}")
    if not Path(configs['repo']).exists():
        Path(configs['repo']).mkdir(parents=True)
    sh.mv(TEMP_FILE, Path(configs['repo']) / fn)
    update_attachments(fn)


def update_note(no: int):
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    fn = paths[no - 1]
    subprocess.run(f'{configs["editor"]} {fn}', shell=True,
                   env={**os.environ, **configs["editor_envs"]})
    updated = datetime.fromtimestamp(
        Path(fn).stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    sh.sed('-i', f'5c Updated: {updated}', fn)
    update_attachments(fn)
    logger.info(list_notes(DEFAULT_NOTE_LIST))


def view_note(no: int):
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    fn = paths[no - 1]
    subprocess.run(f'{configs["viewer"]} {fn}', shell=True,
                   env={**os.environ, **configs["editor_envs"]})


def parse_note(path: Path) -> dict:
    """ convert note in plain text to a dictionary.
        Line #1 ~ #5 are meta data of the note.
        Line #9 to end is the body.
    """
    header_line_number = 5
    body_start_line = 9
    res = {}
    with open(path) as f:
        for x in range(header_line_number):
            the_line = next(f).strip()
            if the_line.endswith(':'):
                the_line += ' '  # fix 'Tags: ' striped to 'Tags:' problem
            header_sections = the_line.split(': ')
            assert len(header_sections) == 2
            res[header_sections[0]] = header_sections[1]
    body = sh.sed('-n', f'{body_start_line},$p', path).stdout.decode('utf-8')
    res['body'] = body
    return res


def record_to_details():
    def extract_header(path: Path) -> str:
        note = parse_note(path)
        return (f'{note["Updated"][:10]} {note["Notebook"]}: {note["Title"]} '
                f'[{note["Created"][:10]}] {note["Tags"]}')

    title_line = 'No. Updated, Notebook, Title, Created, Tags'
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    headers = [extract_header(path) for path in paths]
    with_index = [f'{idx + 1}. {ele}' for idx, ele in enumerate(headers)]
    return '\n'.join([title_line, *with_index])


def list_notes(number):
    file_list = sorted(NOTE_FILES, key=lambda f: f.stat().st_mtime,
                       reverse=True)
    with open(REC_FILE, 'w') as f:
        f.write('\n'.join([str(path) for path in file_list[:number]]))
    return record_to_details()


def delete_note(no: int):
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    if not TRASH.exists():
        TRASH.mkdir()
    sh.mv(paths[no - 1], TRASH)


def filter_word(file_list: List[str], word: str) -> List[str]:
    if len(file_list) == 0:
        return []
    try:
        res = sh.grep('-i', '-l', '-E', word, file_list)
    except sh.ErrorReturnCode_1:
        return []
    else:
        return res.stdout.decode('UTF-8').strip().split('\n')


def simple_search(word_list: List[str]) -> List[str]:
    search_res = reduce(filter_word, word_list, list(NOTE_FILES))
    if len(search_res) == 0:
        return ""
    sorted_res = sorted(search_res, key=lambda f: Path(f).stat().st_mtime,
                        reverse=True)
    with open(REC_FILE, 'w') as f:
        f.write('\n'.join([str(path) for path in sorted_res]))
    return record_to_details()


def preview_note(no: int):
    pandoc = shutil.which('pandoc')
    if pandoc is None:
        logger.error('Pandoc not installed?\nInstall it with '
                     '`apt install pandoc before running this command.')
        return
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    fn = paths[no - 1]
    preview_file = Path(fn).parent / 'preview.html'
    sh.pandoc(fn, standalone=True, mathjax=True, toc=True, o=preview_file)
    webbrowser.open(str(preview_file))


def list_notebooks() -> str:
    nbs = sh.uniq(sh.sort(sh.awk('FNR==3 {print $2}', list(NOTE_FILES))))
    # 前提条件：笔记第 3 行 'Notebook:' 与名称之间有空格
    return nbs


def backup_repo(comments: str):
    vcs = Path(configs['repo']) / '.git'
    if not vcs.exists():
        logger.warn('No git repo detected. Create it and try again.')
        # TODO: add instructions here
        return
    logger.info(sh.git('status', _cwd=configs['repo']))
    sync = input('Sync to remote repo? Y/n ') or 'Y'
    if sync == 'Y':
        logger.info(sh.git('add', '-A', _cwd=configs['repo']))
        logger.info(sh.git('commit', '-m', comments, _cwd=configs['repo']))
        logger.info(sh.git('push', _cwd=configs['repo']))


def export_notes(ftype: str):
    if ftype == 'json':
        (Path.cwd() / EXPORT_DIR).mkdir(exist_ok=True)
        for note in NOTE_FILES:
            data = parse_note(note)
            target = Path.cwd() / EXPORT_DIR / (note.stem + '.json')
            with open(target, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
    else:
        logger.warn('Unsupported export file type')


def advanced_search(name: str, tag: str, content: str, book: str) -> str:
    search_res = list(NOTE_FILES)
    if len(str(name)) > 0:
        search_res = filter_word(search_res, f'^Title: .*{name}')
    if len(str(tag)) > 0:
        search_res = filter_word(search_res, f'^Tag: .*{tag}')
    if len(str(book)) > 0:
        search_res = filter_word(search_res, f'^Notebook: .*{book}')
    if len(str(content)) > 0:
        search_res = filter_word(search_res, content)
    if len(search_res) == 0:
        return ""
    sorted_res = sorted(search_res, key=lambda f: Path(f).stat().st_mtime,
                        reverse=True)
    with open(REC_FILE, 'w') as f:
        f.write('\n'.join([str(path) for path in sorted_res]))
    return record_to_details()
