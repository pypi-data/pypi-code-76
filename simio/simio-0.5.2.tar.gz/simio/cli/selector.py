import click
from simio.cli.create_app import create_project

ACTIONS = {
    # fmt: off
    "create-app": create_project
    # fmt: on
}


@click.command()
@click.argument("action", type=click.Choice(list(ACTIONS.keys()), case_sensitive=False))
def select_action(action: str):
    """
    Main CLI. Selects next step that needs to be executed
    :param action:
    :return: result of selected action
    """
    return ACTIONS[action]()


if __name__ == "__main__":
    select_action()  # pylint: disable=no-value-for-parameter
