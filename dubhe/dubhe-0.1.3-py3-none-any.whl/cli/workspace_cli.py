from dubhe.auth import auth
from dubhe.workspace import workspace
import sys


def workspace_list(args):
    au = auth.Auth.load_active()
    wps, err = workspace.Workspace.list_all(au)
    if err is not None:
        print("list workspace error:", err, file=sys.stderr)
        return None

    active_id = workspace.Workspace.load_active_id(au)

    print(f'# Dubhe all workspaces of auth {au.name}:')
    print('# (id)name description')
    for wp in wps:
        active_flag = "*" if wp.workspace_id == active_id else ""
        print(f'({wp.workspace_id}){wp.name:32s} {active_flag:2s} {wp.description}')

    return wps


def workspace_active(args):
    au = auth.Auth.load_active()
    err = workspace.Workspace.store_active(args.id, au, args.skip)
    if err is not None:
        print(f'active workspace error: {err}')
    else:
        print(f'active workspace {args.id} success')
