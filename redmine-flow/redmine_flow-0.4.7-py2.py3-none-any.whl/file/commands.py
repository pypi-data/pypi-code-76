import redminelib
import click
import os


@click.group()
def file():
    pass


@file.command("new")
@click.option("--me", default="Volodymyr SAVCHENKO")
@click.option("--description", default="auto-upload")
@click.argument("file-path")
@click.pass_context
def new(ctx, me, file_path, description):
    click.echo(ctx.obj['project'].id)

    #for f in redminelib.managers.FileManager(ctx.obj['redmine'], redminelib.resources.File).filter(project_id=ctx.obj['project'].id):
    #    print(f)

    #print(dir(ctx.obj['project']), "files")
    #for f in ctx.obj['project'].files:
    #    print(f)

    redmine = ctx.obj['redmine']

    f = redmine.file.create(
        project_id=ctx.obj['project'].id,
        path=file_path,
        filename=os.path.basename(file_path),
        description=description,
        #content_type='text/pdf',
        #version_id=1
    )
    print(f)
    
@file.command("list")
@click.pass_context
def list(ctx):
 #   click.echo(ctx.obj['project'].id)

    for f in ctx.obj['project'].files:
 #       print(f,dir(f))
        #print(issue, issue.assigned_to)
        try:
            click.echo("%12s %10s %15s %s"%(f.author, f.description, f.filename, f.content_url))
            #print("-- to", issue.created_on)
            #print("-- to", issue.assigned_to.__class__)
            #print("-- to", issue.assigned_to.name.__class__)
        except redminelib.exceptions.ResourceAttrError:
            pass
        except Exception as e:
            pass
            #click.echo("unassigned: %s; %s"% ( repr(e)))

def main():
    issues(obj={})

if __name__ == "__main__":
    issues()
