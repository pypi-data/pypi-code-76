import sys

from click import command, echo

from pyquickstart.project import Project


@command()
def main():
    """
    The command line interface for creating a new Python project from a
    template.
    """
    # Create project
    project = Project()
    project.create()

    # Output success message
    echo(f'Success! Created new project under \'{project.path}\'.')

    # Exit program
    sys.exit()
