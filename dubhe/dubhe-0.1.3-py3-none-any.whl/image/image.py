import urllib.parse
import os
import sys
import logging
import mako.template
import shutil
import json
from dubhe.image import context
from dubhe.utils import download
from dubhe.utils import config

Base_url = 'http://dubhe.hellohui.space/static/'
App_info = 'app_info_v1.json'


class Image(object):
    @classmethod
    def create(cls, name: str, overwrite: bool, debug: bool = False) -> str:
        # check app name
        unquote_name = urllib.parse.quote(name, safe="")
        if unquote_name != name:
            return f'Invalid project name: "{name}", should only contain URL-friendly characters'

        pwd = os.getcwd()

        # create app home folder
        home_path = os.path.join(pwd, name)
        if os.path.exists(home_path):
            if not overwrite:
                return f'{name} exists, use -o to overwrite'
        else:
            os.mkdir(name)

        if not debug:
            # get app info
            app_info_url = os.path.join(Base_url, App_info)
            download.download_url(app_info_url, config.HOME, filename=App_info)

            app_info_file = os.path.join(config.HOME, App_info)
            with open(app_info_file, 'r') as f:
                app_info_dict = json.load(f)

            if 'file' not in app_info_dict or 'md5' not in app_info_dict:
                print(f'app_info_file info error, please check your network or {home} files')
                return 1

            template_url = os.path.join(Base_url, app_info_dict['file'])
            extract_root = os.path.join(config.HOME, app_info_dict['file'] + "_")
            download.download_and_extract_archive(template_url, config.HOME,
                                                  filename=app_info_dict['file'],
                                                  extract_root=extract_root,
                                                  md5=app_info_dict['md5'])
        else:
            root = os.path.split(os.path.abspath(sys.argv[0]))[0]
            extract_root = os.path.join(root, 'app_template')
            logging.debug(f"debug mode, extract from {extract_root}")

        ctx = context.Context()
        ctx.app_name = name

        for root, dirs, files in os.walk(extract_root):
            rel_path = os.path.relpath(root, extract_root)

            base_path = os.path.join(home_path, rel_path)
            if not os.path.exists(base_path):
                os.mkdir(base_path)

            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(base_path, file)

                try:
                    template = mako.template.Template(filename=src_path, input_encoding='utf-8')
                    with open(dst_path, 'w') as f:
                        f.write(template.render(ctx=ctx))
                except:
                    shutil.copyfile(src_path, dst_path)

        return None
