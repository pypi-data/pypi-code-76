import redminelib
import click


@click.group()
def issues():
    pass


@issues.command("list")
@click.option("--me", default="Volodymyr SAVCHENKO")
@click.pass_context
def list_active(ctx, me):
    click.echo(ctx.obj['project'].id)
    
    for issue in ctx.obj['project'].issues:
        #print(issue, issue.assigned_to)
        try:
            if issue.assigned_to.name.lower() == me.lower():
                click.echo("%12s %10s %15s %s"%(issue.created_on, issue.priority, issue.status, issue))
                #print("-- to", issue.created_on)
                #print("-- to", issue.assigned_to.__class__)
                #print("-- to", issue.assigned_to.name.__class__)
        except redminelib.exceptions.ResourceAttrError:
            pass
        except Exception as e:
            click.echo("unassigned: %s; %s"% (issue, repr(e)))


def main():
    issues(obj={})

if __name__ == "__main__":
    issues()
