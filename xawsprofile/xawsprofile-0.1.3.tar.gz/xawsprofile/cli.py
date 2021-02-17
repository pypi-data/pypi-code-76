import click
import sys

from xawsprofile import aws
from xawsprofile import __version__ as VERSION


@click.command(name="list")
def list_profiles():
    profiles = list(aws.get_profiles().keys())
    sys.stdout.write('\n'.join(profiles))


@click.command(name="completion")
@click.argument('shell', required=False)
def completion(shell):
    sys.stdout.write('''_awsprofile()
{
    local cur="${COMP_WORDS[COMP_CWORD]}"
    opts=$(awsprofile list)
    COMPREPLY=( $(compgen -W "$opts" -- $cur) )
}
ap(){
    PROFILE=$1
    PROFILE_ALIAS=$2
    eval $(awsprofile set "$PROFILE" --alias "$PROFILE_ALIAS")
    export PS1='%{$fg[cyan]%}${AWS_PROFILE}%{$reset_color%}> '
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


@click.command(name="set")
@click.argument('name')
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
