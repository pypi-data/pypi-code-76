# coding: utf-8
"""Console script for dgo."""
import sys
import os
import click
import requests
import platform


def get_platform():
    pl = platform.platform().lower()
    if 'ubuntu' in pl:
        return 'ubuntu'
    elif 'centos' in pl:
        return 'centos'
    elif 'darwin' in pl or 'mac' in pl:
        return 'mac'
    else:
        return 'others'


@click.group()
def main(args=None):
    return 0


@main.command()
@click.argument(u'local_file_path', type=click.File('rb'))
def upload(local_file_path):
    u"""
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
@click.argument(u'url')
def wget(url):
    u"""wget with usual params."""
    cmd = "wget --content-disposition \"%s\"" % url
    os.system(cmd)


@main.command()
def pipconf():
    u"""创建pip 配置文件，使用国内镜像
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
    u"""pypirc配置文件"""
    pypirc_path = os.path.expanduser('~/.pypirc')
    if os.path.exists(pypirc_path):
        click.secho(u'~/.pypirc 文件已经存在', fg='red')
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
    click.secho(u'~/.pypirc 生成完毕。', fg='green')


@main.command()
def pyenv():
    """安装 pyenv 环境（当前账号）"""
    if not os.path.exists(os.path.expanduser('~/.pyenv')):
        click.secho(u'现在开始安装 pyenv 环境...', fg='cyan')
        cmd = "curl http://file.daimon.cc/group1/M00/00/11/oYYBAGARMEaAc51mAAABLdrf0TM30.html | bash"
        os.system(cmd)
    with open(os.path.expanduser('~/.pyenv_profile'), 'w') as fout:
        fout.write("""
# User specific aliases and functions
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

""")

    click.secho(u'安装 python 依赖...;', fg='cyan')
    pl = get_platform()
    if pl == 'centos':
        cmd = 'sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel'
    elif pl == 'ubuntu':
        cmd = 'sudo apt-get install -y libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev uuid-dev libffi-dev'
        click.secho(u'如果是 Buster 版本，请继续运行：sudo apt-get install libgdbm-compat-dev', fg='yellow')
    elif pl == 'mac':
        cmd = 'brew install tcl-tk'
        click.secho(u'''mac如果要用tcl，编译的时候要用下面的命令:
env \\
  PATH="$(brew --prefix tcl-tk)/bin:$PATH" \\
  LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \\
  CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \\
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \\
  CFLAGS="-I$(brew --prefix tcl-tk)/include" \\
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \\
  pyenv install 3.8.1
    ''')
    else:
        cmd = 'echo "无法识别的操作系统版本"'
    os.system(cmd)
    if not os.path.exists(os.path.expanduser('~/.pyenv/cache/Python-2.7.18.tar.xz')):
        click.secho(u'现在开始安装 python 2.7.18 环境 ...')
        os.system(
            'mkdir -p ~/.pyenv/cache && cd ~/.pyenv/cache && wget --content-disposition http://file.daimon.cc/group1/M00/00/0B/oYYBAF9xSdeAKkoMAMQl0AMemAM1710.xz?filename=Python-2.7.18.tar.xz')
    os.system('. ~/.pyenv_profile && pyenv install 2.7.18')
    if not os.path.exists(os.path.expanduser('~/.pyenv/cache/Python-3.8.6.tar.xz')):
        click.secho(u'现在开始安装 python 3.8.6 环境 ...')
        os.system(
            'mkdir -p ~/.pyenv/cache && cd ~/.pyenv/cache && wget --content-disposition http://file.daimon.cc/group1/M00/00/0D/oYYBAF_VbI6AdPRMARY6CAOTD6M0836.xz?filename=Python-3.8.6.tar.xz')
    os.system('. ~/.pyenv_profile && pyenv install 3.8.6')


@main.command()
def goenv():
    u"""go 国内镜像"""
    content = u"""
go env -w GO111MODULE=on
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
# go 官方
# go env -w  GOPROXY=https://goproxy.io,direct
"""
    click.secho(content, fg='cyan')


@main.command()
@click.option(u'--input', u'-i', u'input_path', help=u'输入文件路径')
def enc(input_path):
    u"""加密。如果提供了 input_path，则对指定文件加密。否则从 stdin 读数"""
    extra = ""
    if input_path:
        extra = u'-in "%s" -out "%s.enc"' % (input_path, input_path)
    salt_key = click.prompt(u'请输入Key: ', hide_input=True)
    cmd = u'openssl aes-256-cbc -k %s -a -md md5 -base64 %s' % (salt_key, extra)
    os.system(cmd)


@main.command()
@click.option(u'--input', u'-i', u'input_path', help=u'输入文件路径')
def dec(input_path):
    u"""解密。如果提供了 input_path，则对指定文件解密。否则从 stdin 读数"""
    extra = ""
    if input_path:
        extra = u'-in "%s" -out "%s.dec"' % (input_path, input_path)
    salt_key = click.prompt(u'请输入Key: ', hide_input=True)
    cmd = u'openssl aes-256-cbc -k %s -a -md md5 -base64 -d %s' % (salt_key, extra)
    os.system(cmd)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
