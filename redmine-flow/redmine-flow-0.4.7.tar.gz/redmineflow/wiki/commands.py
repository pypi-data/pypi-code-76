import redminelib
import click
import yaml
import os
import re
import glob
import subprocess

import pypandoc

import redmineflow.redmine as remine_flow_core

class repoconf:
    @staticmethod
    def read():
        try:
            repoconf=yaml.safe_load(open("redmine-wiki.yaml"))
        except Exception as e:
            print("no repo conf", e)
            repoconf={}

        return repoconf

    @staticmethod
    def write(rc):
        open("redmine-wiki.yaml", "w").write(yaml.dump(rc, sort_keys=True, indent=4))

    @staticmethod
    def update(rc):
        orc = repoconf.read()
        orc.update(rc)

        repoconf.write(orc)


@click.group()
def wiki():
    pass


@wiki.command("list")
@click.option("--me", default="Volodymyr SAVCHENKO")
@click.pass_context
def list(ctx, me):
    click.echo(ctx.obj['project'].id)

    #for f in redminelib.managers.FileManager(ctx.obj['redmine'], redminelib.resources.File).filter(project_id=ctx.obj['project'].id):
    #    print(f)

    #print(dir(ctx.obj['project']), "files")
    #for f in ctx.obj['project'].files:
    #    print(f)

    #redmine = ctx.obj['redmine']
    
    redmine = ctx.obj['redmine']


    n=0
    for page in redmine.wiki_page.filter(project_id=ctx.obj['project'].id):
        print(page)


        for f in dir(page):
            print("--- ", f, page[f])


        print(page)
        #print(page['author_id'])

        n+=1
        if n>4: break

 #   redminelib.managers.ResourceManager.get(ctx.obj['redmine'], 63)

    return


@wiki.command()
@click.argument("regex", default=None)
@click.option("--title", default=None, help="page title (else current)")
@click.option("--commit", default=False, is_flag=True, help="only actually delete if this is set, else preview")
@click.pass_context
def delete_attachments(ctx, regex, title, commit):
    redmine = ctx.obj['redmine']

    rc = repoconf.read()
    if title is None:
        if  'title' not in rc:
            print("no title in command line or repo config")
            return
        else:
            title = rc['title']
            print("using config title:", title)

    page = redmine.wiki_page.get(
                title, 
                project_id=ctx.obj['project'].id,
                include=["attachments"],
            )

    for attachment in page.attachments:
        print("found attachment:", attachment, attachment.__class__)
        if re.match(regex, str(attachment)):
            print("deleting!")
            if commit:
                attachment.delete()
            else:
                print("(not really)")

@wiki.command()
@click.option("--title", default=None, help="page title (else current)")
@click.option("--local-name", default="README.md")
@click.option("--include-attachments", default=True)
@click.pass_context
def pull(ctx, title, local_name, include_attachments):
    redmine = ctx.obj['redmine']

    rc = repoconf.read()
    if title is None:
        if 'title' not in rc:
            print("no title in command line or repo config")
            return
        else:
            title = rc['title']
            print("using config title:", title)




    page = redmine.wiki_page.get(
                title, 
                project_id=ctx.obj['project'].id,
                include=["attachments"] if include_attachments else [],
            )

    open(local_name, "w").write(page.text)

    for attachment in page.attachments:
        print("found attachment:", attachment, attachment.__class__)
        attachment.download(savepath="./attachments")

    repoconf.update(dict(
        project_id = ctx.obj['project'].id,
        project_name = ctx.obj['project'].name,
        url = f"{remine_flow_core.redmine_url}/projects/{ctx.obj['project'].name}/wiki/{title.replace(' ', '_')}",
        title = title,
        local_name=local_name,
        upstream_type = 'redmine_wiki',
    ))



@wiki.command()
@click.option("--title", help="page title, unless found in redmine-wiki.yaml")
@click.option("--create/--no-create", default=False, help="what to do if the page does not exist")
@click.option("--upload-attachments", is_flag=True, default=False, help="upload all files in \"./attachments/\" as attachments")
@click.pass_context
def push(ctx, title, create, upload_attachments):
    redmine = ctx.obj['redmine']

    rc = repoconf.read()
    if title is None:
        if  'title' not in rc:
            print("no title in command line or repo config")
            return
        else:
            title = rc['title']
            print("using config title:", title)

    text = open(rc['local_name']).read()

    text = pypandoc.convert_text(text, 'textile', format='gfm')

    text += "\n\n*META:* git revision: "+subprocess.check_output(["git", "describe", "--always", "--tags"]).decode()
    text += "\n*META:* git commit time: "+subprocess.check_output(["git", "show", "-s", "--format=%ci"]).decode()
    text += "\n*META:* git : "+subprocess.check_output(["git", "show", "-s", "--format=%ci"]).decode()
    open(".redminified-"+rc['local_name'],"w").write(text)
    
    try:
        page = redmine.wiki_page.get(title, project_id=ctx.obj['project'].id)

        open(".upstream-"+rc['local_name'], "w").write(page.text)

        os.system("colordiff -Z %s %s"%(
                ".upstream-"+rc['local_name'],
                ".redminified-"+rc['local_name'],
        ))
    except redminelib.exceptions.ResourceNotFoundError:
        if not create:
            raise Exception("page %s does not exist in project %s"%(title, str(ctx.obj['project'])))

    uploads = []

    if upload_attachments:
        #[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
        for fn in sorted(glob.glob("attachments/*")):
            print("found file to attach:", fn)
            uploads.append({
                    'path': fn,
                    'filename': os.path.basename(fn),
                    'description': '',
                    'content_type': 'image/png',
                })

    page = redmine.wiki_page.update(title, text=text, project_id=ctx.obj['project'].id, uploads=uploads)
    print("succesfully updated!")


def main():
    issues(obj={})

if __name__ == "__main__":
    issues()
