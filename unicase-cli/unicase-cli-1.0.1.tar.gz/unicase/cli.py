#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2021/2/21 18:15
from pathlib import Path

import click
from terminal_layout import Fore
from terminal_layout.extensions.choice import Choice, StringStyle

from unicase import utils

CONFIG = utils.Config()
CONFIG_DATA = CONFIG.get() or {}
CONFIG_DATA.setdefault('base_url', utils.TAPD_BASE_URL)


@click.group()
def cli():
    """UNI 测试用例管理工具"""


@cli.command()
@click.option('--tester', required=False, help='当前测试人员英文名')
@click.option('--base-url', required=False, help='当前 API Base Url')
def config(tester, base_url):
    """配置测试人员、API Base Url"""
    if tester:
        CONFIG_DATA['tester'] = tester
        click.echo(click.style(f'当前配置的测试人员：{tester}', fg='blue', bold=True))
    if base_url:
        CONFIG_DATA['base_url'] = base_url
        click.echo(click.style(f'当前配置的 Base Url：{base_url}', fg='blue', bold=True))
    if tester or base_url:
        CONFIG.put(CONFIG_DATA)
    else:
        click.echo(click.style(f'tester={CONFIG_DATA.get("tester") or "未配置"}', fg='blue', bold=True))
        click.echo(click.style(f'base_url={CONFIG_DATA.get("base_url")}', fg='blue', bold=True))
        click.echo(
            click.style(f'请输入 unicase --tester <name> 或 unicase --base-url <base url> 进行配置', fg='blue', bold=True))


@cli.command()
@click.option('--name', required=False, help='指定生成的文件路径，默认生成到当前文件夹且已迭代名称命名')
def create(name):
    """创建 Excel 用例模板文件"""
    tapd = utils.Tapd(CONFIG_DATA.get('base_url'))
    iterations = tapd.get_tapd_iterations()

    select = Choice('请选择用例所属的迭代: (按 <esc> 退出) ',
                    list(iterations.keys()),
                    icon_style=StringStyle(fore=Fore.blue),
                    selected_style=StringStyle(fore=Fore.blue))

    choice = select.get_choice()
    if choice:
        index, iteration_name = choice
        target_file_path = Path(name) if name else Path('./').joinpath(utils.secure_filename(iteration_name) + '.xlsm')
        tapd.set_iteration_id(iterations[iteration_name])
        excel = utils.Excel(utils.TEMPLATE_XLS, tapd)
        excel.set_sheet_name(iteration_name)
        excel.set_categories_data_validation()
        excel.set_developer_data_validation()
        excel.set_stories_data_validation()
        excel.save(target_file_path)
        click.echo(click.style(str(target_file_path.absolute()), fg='green', bold=True))


@cli.command()
@click.option('--name', required=True, help='当前测试人员英文名(上传用例时需要用到)')
@click.option('--type', default='bvt', type=click.Choice(['bvt', 'all'], case_sensitive=False), help='用例上传类型')
@click.pass_context
def upload(ctx, name, type):
    """上传 Excel 用例到 TAPD"""
    # if CONFIG_DATA.get('tester') is None:
    #     click.echo(click.style('上传用例需要先配置测试人员', fg='blue', bold=True))
    #     ctx.invoke(config)
    click.echo(click.style('功能正在开发中...', fg='blue', bold=True))
