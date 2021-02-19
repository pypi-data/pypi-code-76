import click
from src.Job import Job
from src.CandidateFinder import run_matcher


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--title', '-t', required=True, prompt=True, help='The job title')
@click.option('--skills', '-s', required=False, multiple=True, default=[],
              help='Optional Skills for the job, you can add multiple skills by using -s/-skill')
def match(title, skills):
    """Returns the best matches for the provided Job"""
    job = Job(title=title, skills=skills)
    print(*run_matcher(job=job), sep='')
