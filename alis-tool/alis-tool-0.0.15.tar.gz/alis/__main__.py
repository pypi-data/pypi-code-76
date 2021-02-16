import argparse
import os


def execute_alis_fn(fn, *arguments):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.system('{}/alis.sh {} {}'.format(dir_path, fn, " ".join('"{}"'.format(arg) if arg is not None else '""' for arg in arguments)))

def console_entry_point():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.system('chmod +x {}/alis.sh'.format(dir_path))

    main_parser = argparse.ArgumentParser(description="""
            ALIS (Arch Linux Installer Script)
        
        This tool is a helper to install Arch Linux
      
    Example:
      alis --auto /dev/sda --sec-locale ro_RO
      alis conf admin-user admin admin
      alis install --user admin --pre-config nano docker
    """, formatter_class=argparse.RawTextHelpFormatter)
    main_parser.add_argument('--auto', metavar='DEVICE', dest='device', help="""Install Arch Linux with default options. 
    !!! This will erase DEVICE !!!
    """)
    main_parser.add_argument('--root-pass', metavar='PASSWORD', help="""Root user allays should have a password
    Default: 'admin'""", default='admin')
    main_parser.add_argument('--sec-locale', metavar='LOCALE', help="""The system language is English, second locale set others stuff like: date format, numeric dot etc.
    Default: 'en_US'""")
    main_parser.add_argument('--swap-size', metavar='SIZE', help="""It is used as a second RAM, it is recommended to have one
    Default: 'size of your ram' (It should be provided in MB)""")
    main_parser.set_defaults(execute=lambda args: execute_alis_fn('alis_defaults', args.device, args.root_pass, args.sec_locale, args.swap_size))
    sub_parser = main_parser.add_subparsers()

    parser = sub_parser.add_parser('part', description="Create partition for Arch Linux")
    parser.add_argument('DEVICE')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--alongside', action='store_true', help='Install Arch Linux next to other system. You should have enough space on device without gaps between partitions.')
    group.add_argument('--replace', action='store_true', help='Delete all data from device and create new partitions.')
    parser.set_defaults(execute=lambda args: execute_alis_fn('alis_create_partition', args.DEVICE, args.alongside))

    parser = sub_parser.add_parser('pacstrap', description="Install base and base-devel")
    parser.set_defaults(execute=lambda args: execute_alis_fn('alis_pacstrap'))

    parser = sub_parser.add_parser('install', description="Install other packages with yay, have to be logged with an user or provide one.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--pre-config', action='store_true', help='''
Install and configure packages if exist.
    *** gnome, imwheel, teamviewer, virtualbox, docker, intellij
There is some groups of packages:
    util-packages = (nano zip unzip wget bash-completion openssh seahorse networkmanager-fortisslvpn)
    dev-packages = (maven npm vagrant packer git python python-pip docker virtualbox)
    tools-packages = (google-chrome variety slack-desktop intellij teamviewer)
    all-packages = (util-packages dev-packages tools-packages imwheel gnome)
    ''')
    parser.add_argument('--user', help='User that install packages; used only if you are logged as root.')
    parser.add_argument('package', nargs='*')
    parser.set_defaults(execute=lambda args: execute_alis_fn('alis_install_package', str(args.pre_config), args.user, *args.package))

    conf_parser = sub_parser.add_parser('conf', description="Arch Linux system configuration tool.")
    sub_parser = conf_parser.add_subparsers()
    parser = sub_parser.add_parser('minimum', description="Configure network, password, swap etc.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--root-pass', metavar='PASSWORD', help="""Root user allays should have a password
    Default: 'admin'""", default='admin')
    parser.add_argument('--arch-name', metavar='NAME', help="""System name
    Default: 'archlinux'""", default='archlinux')
    parser.add_argument('--sec-locale', metavar='LOCALE', help="""The system language is English, second locale set others stuff like: date format, numeric dot etc.
    Default: 'en_US'""", default='en_US')
    parser.add_argument('--timezone', metavar='TIMEZONE', help="""It is used to set time by location.
    Default: 'it will be current location'""")
    parser.add_argument('--swap', metavar='SWAP_SIZE', help="""It is used as a second RAM, it is recommended to have one
    Default: 'size of your ram' (It should be provided in MB)""")
    parser.set_defaults(execute=lambda args: execute_alis_fn('alis_config_minimum', args.root_pass, args.arch_name, args.sec_locale, args.swap, args.timezone))
    parser = sub_parser.add_parser('admin-user', description="Set an sudo user", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('username', help="""Admin user name
    Default: 'admin'""", default='admin')
    parser.add_argument('password', help="""Admin user password
    Default: 'admin'""", default='admin')
    parser.set_defaults(execute=lambda args: execute_alis_fn('alis_admin_user', args.username, args.password))


    args = main_parser.parse_args()
    args.execute(args)


if __name__ == '__main__':
    console_entry_point()
