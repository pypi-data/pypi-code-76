from dubhe.auth import auth
from dubhe.workspace import workspace
from dubhe.dataset import dataset
import sys


def dataset_list(args):
    au = auth.Auth.load_active()
    active_wp_id = workspace.Workspace.load_active_id(au)
    wp, err = workspace.Workspace.load(au, active_wp_id)
    if err is not None:
        print("load workspace for list dataset error:", err, file=sys.stderr)
        return None

    dss, err = dataset.Dataset.list_all(au, active_wp_id)
    if err is not None:
        print("list dataset error:", err, file=sys.stderr)
        return None

    print(f'# Dubhe all dataset of workspaces ({active_wp_id}){wp.name} and auth ({au.user_id}){au.name}:')
    print('# (id)name encrypted? description')
    for ds in dss:
        active_flag = "*" if ds.encrypted else ""
        print(f'({ds.dataset_id}){ds.name:32s} {active_flag:2s} {ds.description}')

    return dss


def dataset_checkout(args):
    au = auth.Auth.load_active()

    print(f'checkout dataset {args.id}:')

    def checkout_process():
        print(".", end="")

    dataset.Dataset.checkout(checkout_process, au, args.id)
    print("\nSuccess")
