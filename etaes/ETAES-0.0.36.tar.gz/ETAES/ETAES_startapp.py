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

def startapp(proj_name=g_proj_name, mode='charm'):
    import site
    excute_path = os.path.join(site.getsitepackages()[0], 'ETAES')
    # excute_path = os.getcwd()
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
    # cfg_init_path = os.path.join(cfg_path, '__init__.py')
    # if os.path.exists(cfg_init_path):
    #     shutil.rmtree(cfg_init_path)
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

    if mode == 'charm':
        dst_path_temp = dst_path + 'temp'
        if not os.path.exists(dst_path_temp):
            os.mkdir(dst_path_temp)
        for path in os.listdir(dst_path):
            if os.path.isdir(os.path.join(dst_path, path)):
                for path2 in os.listdir(os.path.join(dst_path, path)):
                    if os.path.isdir(os.path.join(os.path.join(dst_path, path), path2)):
                        shutil.copytree(os.path.join(os.path.join(dst_path, path), path2), os.path.join(dst_path_temp, path2))
            else:
                if path == '__init__.py':
                    shutil.copy(os.path.join(dst_path, path), os.path.join(dst_path_temp, 'main.py'))
                else:
                    shutil.copy(os.path.join(dst_path, path), os.path.join('/'.join(dst_path_temp.split('/')[:-1]), path))
        shutil.rmtree(dst_path)
        shutil.move(dst_path_temp, dst_path)

    return 'Successfully create project %s' % proj_name

if __name__ == '__main__':
    _, proj_name = sys.argv
    g_proj_name = proj_name
    fire.Fire(startapp)