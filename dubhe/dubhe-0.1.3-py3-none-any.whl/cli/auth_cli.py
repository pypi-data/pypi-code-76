from dubhe.auth import auth
import sys


def auth_add(args):
    au = auth.Auth(args.name, args.user, args.token, args.endpoint, is_active=args.active)
    _, _, err_msg = au.renew_token()
    if err_msg is not None:
        print("add auth error:", err_msg, file=sys.stderr)
        return

    au.store()

    if args.active:
        print(f'added auth "{args.name}" and active it success')
    else:
        print(f'added auth "{args.name}" success')

    return au


def auth_list(args):
    auth_list = auth.Auth.load_all()
    print("# Dubhe auths:")
    print("#")
    for au in auth_list:
        active_flag = "*" if au.is_active else ""
        print(f'{au.name:32s} {active_flag:2s} {au.endpoint}')

    return auth_list


def auth_active(args):
    auth_list = auth.Auth.load_all()
    for au in auth_list:
        if au.name == args.name:
            au.is_active = True
            au.store()
            print(f'active auth "{au.name}" success')
            return au

    print(f'auth "{args.name}" not found')
    return None





