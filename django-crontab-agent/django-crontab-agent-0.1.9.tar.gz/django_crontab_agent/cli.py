import click
from . import services

@click.group()
def agent():
    pass


@agent.command(name="sync")
@click.option("-c", "--config", default="/etc/django-crontab-agent/config.yml")
def do_sync(config):
    """Sync agent settings from manager server.
    """
    return services.do_sync(config)

@agent.command(name="reset-cronfile")
@click.option("-c", "--config", default="/etc/django-crontab-agent/config.yml")
def do_reset_crontfile(config):
    """Re-generate cron file for all schedules.
    """
    return services.do_reset_crontfile(config)

@agent.command(name="install")
@click.option("-c", "--config", default="/etc/django-crontab-agent/config.yml")
def do_install(config):
    """Setup auto sync cron job.
    """
    return services.do_install(config)


@agent.command(name="exec")
@click.option("-c", "--config", default="/etc/django-crontab-agent/config.yml")
@click.argument("schedule", nargs=1, required=True)
def do_schedule_exec(config, schedule):
    """Execute schedule job.
    """
    return services.do_schedule_exec(config, schedule)

if __name__ == "__main__":
    agent()
