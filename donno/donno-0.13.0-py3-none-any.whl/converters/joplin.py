from pathlib import Path
from datetime import datetime
import json
import re
import sh
from donno.config import get_attr


configs = get_attr()


def f2dict(fp: str) -> dict:
    with open(fp) as f:
        res = json.load(f)
    return res


def get_slug(notebook: dict, nbs: list) -> str:
    if len(notebook['parent_id']) == 0:
        parent_slug = ''
    else:
        parent_nb = [x for x in nbs
                     if x['id'] == notebook['parent_id']][0]
        parent_slug = get_slug(parent_nb)
    return parent_slug + '/' + notebook['title']


def import_json(import_folder):
    dicts = map(f2dict, Path(import_folder).glob('*.json'))
    notes = []
    notebooks = []
    resources = []
    tags = []
    relations = []

    for adict in dicts:
        if adict['type_'] == 1:
            notes.append(adict)
        elif adict['type_'] == 2:
            notebooks.append(adict)
        elif adict['type_'] == 3:
            print('id:', adict['id'], 'type:', 3)
        elif adict['type_'] == 4:
            resources.append(adict)
        elif adict['type_'] == 5:
            tags.append(adict)
        elif adict['type_'] == 6:
            relations.append(adict)

    for rel in relations:
        the_tag = [x for x in tags if x['id'] == rel['tag_id']][0]
        the_note = [x for x in notes if x['id'] == rel['note_id']][0]
        if 'tag' not in the_note:
            the_note['tag'] = []
        the_note['tag'].append(the_tag['title'])

    for nb in notebooks:
        nb['slug'] = get_slug(nb)

    jop_link = re.compile(r'!\[\w{32}\.(\w{1,5})\]\(:/(\w{32})\)',
                          re.MULTILINE)
    for note in notes:
        nb = [x for x in notebooks if x['id'] == note['parent_id']][0]
        body = re.sub(jop_link, r'![image](resources/\2.\1)', note['body'])
        fn = f"{note['id']}.md"
        tags = note['tag'] if 'tag' in note else ''
        created = datetime.utcfromtimestamp(int(note['user_created_time']) /
                                            1000).strftime('%Y-%m-%d %H:%M:%S')
        updated = datetime.utcfromtimestamp(int(note['user_updated_time']) /
                                            1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f'Write to {fn} ...')
        with open(fn, 'w') as f:
            md_note = (f"Title: {note['title']}\n"
                       f"Tags: {tags}\n"
                       f"Notebook: {nb['slug']}\n"
                       f"Created: {created}\n"
                       f"Updated: {updated}\n"
                       "\n------\n\n") + body
            f.write(md_note)
        sh.mv(fn, configs['repo'])
