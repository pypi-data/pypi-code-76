#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : python meutils/clis/__init__.py


import typer

from meutils.pipe import *
from meutils.zk_utils import get_zk_config

cli = typer.Typer(name="MeUtils CLI")


@cli.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@cli.command()
def zk2file(zk_path, mode='yaml', filename=None):
    """本地可再同步到hdfs

     mecli zk2file /mipush/zk2yaml/train.yaml --mode yaml --filename new.yaml

    :param zk_path:
    :param mode:
    :param filename: 不为空可覆盖
    :return:
    """
    zk_conf = get_zk_config(zk_path, mode=mode)

    if filename is None:
        filename = zk_path.split('/')[-1]

    with open(filename, 'w') as f:
        if mode == 'yaml':
            yaml.dump(zk_conf, f)
        else:
            f.write(zk_conf.decode())


@cli.command()
def zk2yaml(zk_path):
    """本地可再同步到hdfs

    :param zk_path: /mipush/zk2yaml/train.yaml
    :return:
    """
    yaml_path = zk_path.split('/')[-1]
    if Path(yaml_path).is_file():
        yaml_conf = yaml_load(yaml_path)  # 读取本地同步的文件
    else:
        yaml_conf = ''
    zk_conf = get_zk_config(zk_path)

    if zk_conf != yaml_conf:  # 对比线上线下文件，更新了则执行重写
        logger.info('\n' + bjson(zk_conf))
        with open(yaml_path, 'w') as f:
            yaml.dump(zk_conf, f)


if __name__ == '__main__':
    cli()
