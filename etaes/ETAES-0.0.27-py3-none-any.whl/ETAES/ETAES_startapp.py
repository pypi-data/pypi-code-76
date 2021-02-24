#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :ETAES_startapp.py
# @Time     :2021/2/22
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None


import os
import shutil
import sys
import fire

g_proj_name = 'project'

def startapp(proj_name=g_proj_name):
    import site
    # excute_path = os.path.join(site.getsitepackages()[0], 'ETAES')
    excute_path = os.getcwd()
    print(excute_path)
    sys.path.append(excute_path)
    ori_path = os.path.join(excute_path, 'prototype')
    dst_path = os.path.join(os.getcwd(), proj_name)
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    shutil.copytree(ori_path, dst_path)
    shutil.move(os.path.join(dst_path, 'prototype'), os.path.join(dst_path, 'prototype').replace('prototype', proj_name))

    replace_paths = {}
    cfg_path = os.path.join(dst_path, f'{proj_name}/cfgs/config.yaml.py')
    replace_paths['cfg_path'] = cfg_path
    install_sh_path = os.path.join(dst_path, 'install.sh.py')
    replace_paths['install_sh_path'] = install_sh_path
    readme_md_path = os.path.join(dst_path, 'README.md.py')
    replace_paths['readme_md_path'] = readme_md_path
    readme_cn_md_path = os.path.join(dst_path, 'README_CN.md.py')
    replace_paths['readme_cn_md_path'] = readme_cn_md_path
    requirements_path = os.path.join(dst_path, 'requirements.txt.py')
    replace_paths['requirements_path'] = requirements_path

    for _, path_value in replace_paths.items():
        if os.path.exists(path_value):
            shutil.move(path_value, path_value.replace('.py',''))


    return 'Successfully create project %s' % proj_name

if __name__ == '__main__':
    _, proj_name = sys.argv
    g_proj_name = proj_name
    fire.Fire(startapp)