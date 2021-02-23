import sys
import os
from pathlib import Path
import shutil
import subprocess

import requests
import typer

app = typer.Typer()

VENV_NAME = "magic_venv"

REPO_NAME = "jerber/MagicAPI-Boilerplate"

MAIN_FILENAME = "main.py"

START_FILENAME = "start.py"


@app.command()
def sowell():
    """
    Load the portal gun
    """

    typer.echo("IS GOAT")


def download_boilerplate_git_folder(output_filename):
    github_repo_url = f"https://api.github.com/repos/{REPO_NAME}/tarball/master"
    r = requests.get(github_repo_url, stream=True)
    with open(output_filename, "wb") as f:
        for chunk in r.raw.stream(1024, decode_content=False):
            if chunk:
                f.write(chunk)


def make_venv(venv_name: str = VENV_NAME):
    os.system(f"python3 -m venv {venv_name}")
    os.system(f"source {venv_name}/bin/activate && pip install -r requirements.txt")


@app.command()
def create(project_name: str = typer.Argument("magic-server"), replace: bool = False):
    # TODO add some printing of status
    project_path = Path(project_name)
    if project_path.exists() and not replace:
        typer.secho(
            "There is already a project that exists with this name. If you would like to replace this project, "
            "add the flag --replace to your command",
            fg=typer.colors.MAGENTA,
        )
        raise typer.Exit()

    zip_filename = "boilerplate.tar.gz"
    download_boilerplate_git_folder(zip_filename)

    temp_dir = Path("._magic_")
    shutil.unpack_archive(zip_filename, temp_dir)
    git_folder = list(temp_dir.glob("*"))[0]

    if project_path.exists():
        shutil.rmtree(project_path)

    git_folder.replace(project_path)

    shutil.rmtree(temp_dir)
    os.remove(zip_filename)

    typer.secho(
        f"Your app {project_name} has been created 🚀. Run 'cd {project_name}' and then "
        f"'magic dev' to start your first magic server 🎩!",
        fg=typer.colors.BRIGHT_GREEN,
    )


@app.command()
def dev(venv_name: str = typer.Argument(VENV_NAME), create_venv: bool = True):
    main_filename = "main.py"
    if not Path(main_filename).exists():
        typer.secho(
            "Cannot find the main.py file. Are you sure you created this app with magic?",
            fg=typer.colors.MAGENTA,
        )
        raise typer.Exit()

    command = f"export LOCAL=1 && python {main_filename}"

    out = subprocess.run(["which", "python"], stdout=subprocess.PIPE)
    interpreter_path = out.stdout.decode("utf-8").strip()

    # if they are using a venv, let them use it, but maybe install everything on it?
    if f"{venv_name}/bin/python" not in interpreter_path and create_venv:
        typer.echo(
            "No venv is active, will check to see if one exists and make one if not."
        )
        venv_path = Path(venv_name)
        if not venv_path.exists():
            typer.echo(f"No venv detected, will make one now with name {venv_name}")
            make_venv(venv_name)
        command = f"source {venv_name}/bin/activate && {command}"

    typer.secho(
        "To get interactive docs, go to http://0.0.0.0:8000/docs 🎩!",
        fg=typer.colors.BRIGHT_GREEN,
    )
    os.system(command)


@app.command()
def start():
    typer.secho(
        "To get interactive docs, go to http://0.0.0.0:8000/docs 🎩!",
        fg=typer.colors.BRIGHT_GREEN,
    )
    command = f"python {START_FILENAME}"
    os.system(command)


@app.command()
def test(url: str = typer.Argument("")):
    os.environ['testing_url'] = url
    command = f"pytest -s -v"
    os.system(command)


@app.command()
def deploy():
    command = f"sls deploy"
    os.system(command)


@app.command()
def deploy_again():
    command = f"sls deploy --function app"
    os.system(command)


@app.command()
def version():
    typer.echo("9")


if __name__ == "__main__":
    app()
