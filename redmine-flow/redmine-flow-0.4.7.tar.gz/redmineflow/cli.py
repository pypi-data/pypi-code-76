import click

from .issues import commands as group1
from .docs import commands as group2
from .file import commands as group3
from .wiki import commands as group4

from redmineflow.redmine import connect
import redminelib

@click.group()
@click.option("--project-name", default="INTEGRAL")
@click.pass_context
def entry_point(ctx, project_name):
    ctx.obj['redmine'] = connect()
    click.echo("connected to redmine {}".format(ctx.obj['redmine']))

    try:
        ctx.obj['project'] = ctx.obj['redmine'].project.get(project_name)
    except redminelib.exceptions.ResourceNotFoundError as e:
        raise Exception("project \"%s\" does not exist"%project_name)
        

    click.echo("selected project {} as {}".format(project_name, ctx.obj['project']))


entry_point.add_command(group1.issues)
entry_point.add_command(group2.docs)
entry_point.add_command(group3.file)
entry_point.add_command(group4.wiki)


def main():
    entry_point(obj={})

if __name__ == "__main__":
    main()
