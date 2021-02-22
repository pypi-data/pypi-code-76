# coding: utf-8
"""Console script for dgo."""
import sys
import os
import click
import requests
import subprocess


@click.group()
def main(args=None):
    return 0


@main.command()
@click.argument('local_file_path', type=click.File('rb'))
def upload(local_file_path):
    """
    Temporary upload a file.
    Then can download it later.
    But not guarantee when to delete from the server.
    So do not upload your importance file here.
    """
    ret = requests.post('http://tmp.daimon.cc:10080/upload', files={
        'file': local_file_path
    })
    click.secho('wget %s' % (ret.text.split(':', 1)[1].strip()), fg='cyan')
    return 0


@main.command()
@click.argument('url')
def wget(url):
    """wget with usual params."""
    cmd = "wget --content-disposition \"%s\"" % url
    os.system(cmd)


@main.command()
def pipconf():
    """创建pip 配置文件，使用国内镜像
    """
    pip_conf_file_content = """
[global]
index-url=https://mirrors.aliyun.com/pypi/simple/
trusted-host=
    mirrors.daimon.cc
    mirrors.cloud.tencent.com
    mirrors.aliyun.com
"""
    with open('/etc/pip.conf', 'w') as fout:
        fout.write(pip_conf_file_content)
    click.secho(u'/etc/pip.conf 文件创建成功', fg='green')


@main.command()
def pypirc():
    """pypirc配置文件"""
    pypirc_path = os.path.expanduser('~/.pypirc')
    if os.path.exists(pypirc_path):
        click.secho('~/.pypirc 文件已经存在', fg='red')
        return 1

    content = """
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: %s
password: %s
"""
    username = click.prompt('username in pypi: ')
    password = click.prompt('password in pypi: ', hide_input=True)
    content = content % (username, password)
    with open(pypirc_path, 'w') as fout:
        fout.write(content)
    click.secho('~/.pypirc 生成完毕。', fg='green')


@main.command()
def goenv():
    """go 国内镜像"""
    content = u"""
go env -w GO111MODULE=on
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
# go 官方
# go env -w  GOPROXY=https://goproxy.io,direct
"""
    click.secho(content, fg='cyan')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
