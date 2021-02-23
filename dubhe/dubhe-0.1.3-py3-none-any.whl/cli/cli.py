from dubhe.cli import workspace_cli
from dubhe.cli import auth_cli
from dubhe.cli import sys_cli
from dubhe.cli import dataset_cli
from dubhe.utils import BaseModel
from dubhe.auth import authpo
from dubhe.utils import propertypo
from dubhe.utils import config
from dubhe.dataset import datasetpo
from dubhe.cli import image_cli
import argparse
import logging


def cli_init(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    BaseModel.init_table([authpo.AuthPo, propertypo.PropertyPo, datasetpo.DatasetPo])


def cli_clear():
    BaseModel.clear_table([authpo.AuthPo, propertypo.PropertyPo, datasetpo.DatasetPo])


def cli():
    parser = argparse.ArgumentParser(description='Dubhe1 algorithm code CLI tool',
                                     prog=config.PROG
                                     # formatter_class=lambda prog: argumentHelper.MyHelpFormatter(prog),
                                     # add_help=False,
                                     )
    parser.add_argument("-v", '--version', action='store_true', help="output the version number")
    parser.add_argument('--verbose', action='store_true', help=argparse.SUPPRESS)

    sub = parser.add_subparsers()

    # sys
    sys = sub.add_parser('sys', help='system settings')
    sys_parsers = sys.add_subparsers()

    auth_add_subparsers = sys_parsers.add_parser('clear', help='clear all data')
    auth_add_subparsers.add_argument("-f", '--force', action='store_true', help="force")
    auth_add_subparsers.set_defaults(func=sys_cli.sys_clear)

    # auth
    auth = sub.add_parser('auth', help='login endpoint')
    auth_parsers = auth.add_subparsers()

    auth_add_subparsers = auth_parsers.add_parser('add', help='add a endpoint')
    auth_add_subparsers.add_argument('name', type=str, help='name of endpoint')
    auth_add_subparsers.add_argument("-u", '--user', required=True, type=str, help="userId")
    auth_add_subparsers.add_argument("-t", '--token', required=True, type=str, help="user token")
    auth_add_subparsers.add_argument("-e", '--endpoint', required=True, type=str, help="endpoint, for example:"
                                                                                       "https://api.dubhe.tcl.com/")
    auth_add_subparsers.add_argument("-a", '--active', action='store_true', help="also active current auth")
    # auth_add_subparsers.add_argument('-d', '--debug', action='store_true', help=argparse.SUPPRESS)
    auth_add_subparsers.set_defaults(func=auth_cli.auth_add)

    auth_active_subparsers = auth_parsers.add_parser('active', help='set active endpoint')
    auth_active_subparsers.add_argument('name', type=str, help='name of endpoint')
    auth_active_subparsers.set_defaults(func=auth_cli.auth_active)

    auth_active_subparsers = auth_parsers.add_parser('list', help='list all endpoint')
    auth_active_subparsers.set_defaults(func=auth_cli.auth_list)

    # workspace
    work_space = sub.add_parser('workspace', help='set workspace')
    workspace_parsers = work_space.add_subparsers()

    workspace_list_parsers = workspace_parsers.add_parser('list'
                                                          , help='update and list all workspace of active endpoint')
    workspace_list_parsers.set_defaults(func=workspace_cli.workspace_list)

    workspace_list_parsers = workspace_parsers.add_parser('active', help='set active workspace')
    workspace_list_parsers.add_argument('id', type=str, help='id of workspace')
    workspace_list_parsers.add_argument("-s", '--skip', action='store_true', help="do not check if workspace is valid")

    workspace_list_parsers.set_defaults(func=workspace_cli.workspace_active)

    # Dataset
    dataset = sub.add_parser('dataset', help='set dataset')
    dataset_parsers = dataset.add_subparsers()

    dataset_list_parsers = dataset_parsers.add_parser('list'
                                                      , help='update and list all dataset of active workspace')
    dataset_list_parsers.set_defaults(func=dataset_cli.dataset_list)

    dataset_list_parsers = dataset_parsers.add_parser('checkout'
                                                      , help='checkout a dataset')
    dataset_list_parsers.add_argument('id', type=str, help='id of dataset')
    dataset_list_parsers.set_defaults(func=dataset_cli.dataset_checkout)

    # Image
    image = sub.add_parser('image', help='commands on algorithm image')
    image_parsers = image.add_subparsers()

    image_create = image_parsers.add_parser('create'
                                            , help='create a new project powered by %(prog)s')
    image_create.add_argument('app_name', type=str, help='app-name')
    image_create.add_argument("-o", '--overwrite', action='store_true', help="overwrite if exists")
    image_create.add_argument('-d', '--debug', action='store_true', help=argparse.SUPPRESS)
    image_create.set_defaults(func=image_cli.image_create)

    image_run = image_parsers.add_parser('run'
                                         , help='run a project powered by %(prog)s')
    image_run.add_argument('-m', '--method', type=str, required=True, help="method, train or predict")
    image_run.add_argument('-i', '--id', type=str, help="algorithm id to run, default: the main one")
    image_run.add_argument('--input_train', type=str, required=False, help="input train dataset id for train only")
    image_run.add_argument('--input_valid', type=str, required=False, help="input valid dataset id for train only")
    image_run.add_argument('--input_test', type=str, required=False, help="input test dataset id for predict only")
    image_run.add_argument('--output', type=str, help="output dataset id for predict only"
                                                      "output file write file will be ignored if not specified ")
    image_run.add_argument('-d', '--debug', action='store_true', help=argparse.SUPPRESS)
    image_run.set_defaults(func=image_cli.image_run)

    args = parser.parse_args()
    # print(args.py)
    if 'func' in args:
        cli_init(args)
        return args.func(args)
    elif args.version:
        print(f'{config.PROG} {config.VERSION}')
    else:
        parser.print_help()
