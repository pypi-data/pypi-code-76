import click
import os
import sys
import subprocess

from xawsprofile import aws
from xawsprofile import __version__ as VERSION


@click.command(name="list")
def list_profiles():
    profiles = list(aws.get_profiles().keys())
    sys.stdout.write('\n'.join(profiles))


def shell_autocomplete(ctx, args, incomplete):
    options = ['bash', 'zsh']
    return [c for c in options if incomplete in c[0]]


@click.command(name="completion")
@click.argument('shell', required=False, autocompletion=shell_autocomplete)
def completion(shell):
    env = {
        '_AWSPROFILE_COMPLETE': f'source_{shell}',
        'PATH': os.environ.get('PATH', '')
    }
    output = subprocess.run(["awsprofile"], env=env, stdout=subprocess.PIPE)
    sys.stdout.write(output.stdout.decode())

    if shell == 'zsh':
        sys.stdout.write('''
_awsprofile()
{
    local cur="${COMP_WORDS[COMP_CWORD]}"
    opts=$(awsprofile list)
    COMPREPLY=( $(compgen -W "$opts" -- $cur) )
}
ap(){
    PROFILE=$1
    PROFILE_ALIAS=$2
    eval $(awsprofile set "$PROFILE" --alias "$PROFILE_ALIAS")
    export PS1='${AWS_PROFILE} (${AWS_DEFAULT_REGION})> '
}
_awsregion()
{
    local cur="${COMP_WORDS[COMP_CWORD]}"
    opts=$(awsprofile list-regions)
    COMPREPLY=( $(compgen -W "$opts" -- $cur) )
}
ar(){
    REGION=$1
    export AWS_DEFAULT_REGION=$REGION
}
complete -F _awsprofile ap
complete -F _awsregion ar''')
    sys.stdout.flush()


def get_profiles(ctx, args, incomplete):
    options = aws.get_profiles().keys()
    return [c for c in options if incomplete in c[0]]


@click.command(name="set")
@click.argument('name', autocompletion=get_profiles)
@click.option('--alias', required=False, help='Name of the alias to save this as.')
def set_profile(name, alias):
    profiles = aws.get_profiles()
    profile_name = profiles.get(name, None)
    if profile_name is None:
        sys.stderr.write(f"profile {name} or alias not found\n")
        exit(1)
    if alias:
        aws.save_alias(profile_name, alias)
    sys.stdout.write(f"export AWS_PROFILE=\"{profile_name}\"")


def get_config_names(ctx, args, incomplete):
    options = ['cwd']
    return [c for c in options if incomplete in c[0]]


# awsprofile config cwd --match 'test-(.*)' --replace \1
@click.command(name="config")
@click.argument('name', autocompletion=get_config_names)
@click.option('--match', required=True, help='Regular expression to match profile name')
@click.option('--replace', default=r'\1', help=r'Replace expression (\1, \2, etc for groups)')
@click.option('--negate', flag_value=True, help='Use to negate the match (check for false)')
@click.option('--visible', flag_value=True, default=True, help='Use to show/hide profiles')
def config_cli(name, match, replace, negate, visible):
    if name == 'cwd':
        aws.save_current_naming(match, replace_with=replace)
    else:
        click.echo('config %s not supported' % name, err=True)


@click.command(name="list-regions")
def list_regions():
    sys.stdout.write('\n'.join(aws.get_regions()))


def version():
    return VERSION


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def main():
    pass

main.add_command(list_profiles)
main.add_command(set_profile)
main.add_command(completion)
main.add_command(list_regions)
main.add_command(config_cli)
