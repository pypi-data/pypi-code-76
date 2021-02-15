def get_shell(host):
    result = host.exec("awk -F: -v user=`whoami` '$1 == user {print $NF}' /etc/passwd")
    return result.stdout.decode().strip()


def get_shell_rc_file(host):
    shell = get_shell(host)
    if shell == "/bin/zsh":
        return "~/.zshrc"
    elif shell == "/bin/bash":
        return "~/.bashrc"
    else:
        raise Exception(f"Unknown shell ({shell})")



