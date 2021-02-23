import click

from MyVault.src import Vault


def db_path_config_path(is_mandatory: bool = False, change_config: bool = False):
    def decorator(function):
        function = click.option(
            "--db",
            required=True,
            type=click.Path(dir_okay=False, exists=is_mandatory),
            help="Path to the vault database.",
        )(function)
        function = click.option(
            "--config",
            required=True,
            type=click.Path(dir_okay=False, exists=True),
            help="Path to the encryption config file.",
        )(function)
        if change_config is True:
            function = click.argument(
                "new-config", type=click.Path(dir_okay=False, exists=True)
            )(function)
        return function

    return decorator


def folder_name(function):
    function = click.argument("folder", default="None", type=str)(function)
    function = click.argument("name", type=str)(function)
    return function


@click.group()
def main():
    pass


@main.command(help="Add a secret (will be prompted) to the vault.")
@db_path_config_path(is_mandatory=False, change_config=False)
@folder_name
def add(db: str, config: str, folder: str, name: str):
    secret = click.prompt(
        text="Secret to be added to the vault",
        confirmation_prompt=True,
        hide_input=True,
    )
    with Vault(db_path=db, config_path=config) as vault:
        vault.upsert(folder=folder, name=name, secret=secret)


@main.command(help="Copy the decrypted secret from the vault to the clipboard.")
@db_path_config_path(is_mandatory=True, change_config=False)
@folder_name
def copy(db: str, config: str, folder: str, name: str):
    with Vault(db_path=db, config_path=config) as vault:
        vault.copy(folder=folder, name=name)


@main.command(help="List all the folders and names of secrets.")
@db_path_config_path(is_mandatory=True, change_config=False)
def list(db: str, config: str):
    with Vault(db_path=db, config_path=config) as vault:
        vault.list_()


@main.command(help="Update encryption configuration for the vault.")
@db_path_config_path(is_mandatory=True, change_config=True)
def update(db: str, config: str, new_config: str):
    with Vault(db_path=db, config_path=config) as vault:
        vault.update_encryption(new_config_path=new_config)


@main.command(help="Delete a secret by its folder and name.")
@db_path_config_path(is_mandatory=True, change_config=False)
@folder_name
def remove(db: str, config: str, folder: str, name: str):
    with Vault(db_path=db, config_path=config) as vault:
        vault.remove(folder=folder, name=name)


commands = click.CommandCollection(sources=[main])


if __name__ == "__main__":
    commands()
