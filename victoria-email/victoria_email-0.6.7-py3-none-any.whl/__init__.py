"""victoria_email

A Victoria plugin for managing the FileTrust Rebuild for Email platform.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import logging
from typing import List

import aiorun
import click
from victoria.plugin import Plugin

from victoria_email.core.util import generate_random_email

from . import load_test, schemas, reconstruct_mail, replay_deadletters, recover_mail, send_mail


def ensure_mailtoil(cfg: schemas.EmailConfig) -> None:
    """Logs an error and exits if mailtoil is not present in config."""
    if cfg.mail_toil is None:
        logging.error(
            "You need to configure the 'mail_toil' section of your config to use this command!"
        )
        raise SystemExit(1)


def ensure_loadtest(cfg: schemas.EmailConfig) -> None:
    """Logs an error and exits if loadtest is not present in config."""
    if cfg.load_test is None:
        logging.error(
            "You need to configure the 'mail_toil' section of your config to use this command!"
        )
        raise SystemExit(1)


@click.group()
def root_cmd() -> None:
    """Perform various actions on the Rebuild for Email platform."""


@root_cmd.command()
@click.option(
    "-n",
    "--frequency",
    type=int,
    required=False,
    default=1,
    help="The number of emails to send per second of the test. Default: 1.")
@click.option("-e",
              "--endpoint",
              type=str,
              required=True,
              help="The SMTP endpoint (and optional port) to send to.")
@click.option("-t",
              "--duration",
              type=int,
              required=False,
              default=1,
              help="The duration in seconds of the test. Default: 1.")
@click.option("-r",
              "--recipient",
              type=str,
              default=generate_random_email(),
              help="The email recipient address. Default: A random email recipient will be generated")
@click.option("-s",
              "--sender",
              type=str,
              required=True,
              default=generate_random_email(),
              help="The email sender address. Default: A random email sender will be generated")
@click.option("-i",
              "--tenant_ids",
              type=str,
              multiple=True,
              required=False,
              default=None,
              help="Tenant id. Default: A random tenant id will be generated")
@click.pass_obj
def loadtest(cfg: schemas.EmailConfig, frequency: int, endpoint: str,
             duration: int, recipient: str, sender: str, tenant_ids: list) -> None:
    """Perform a load test on a cluster.
    
    \b
    Send a single email:
    $ victoria email loadtest -e smtp.example.com -s test@example.com -r test@example.com

    \b
    Send 46 mails per second for 60 seconds:
    $ victoria email loadtest -e smtp.example.com -n 46 -t 60 -s test@example.com -r test@example.com

    \b
    Send using a different port than port 25:
    $ victoria email loadtest -e smtp.example.com:465 -s test@example.com -r test@example.com
    """
    loop = aiorun.get_event_loop()
    loop.set_exception_handler(lambda loop, context: "Error")
    loop.run_until_complete(
        load_test.perform_load_test(frequency, endpoint, duration, recipient,
                                    sender, tenant_ids, cfg.load_test, cfg))


@root_cmd.command()
@click.argument("cluster", nargs=1, type=str)
@click.option("-o",
              "--output",
              type=str,
              required=True,
              help="The directory to write reconstructed mail to.")
@click.option("-a", "--anon", type=bool, is_flag=True)
@click.option("-id",
              "--transaction-id",
              multiple=True,
              type=str,
              help="Cherry-pick GUIDs from blob storage to reconstruct. "
              "This bypasses dead letter scanning.")
@click.pass_obj
def reconstruct(cfg: schemas.EmailConfig, cluster: str, output: str,
                anon: bool, transaction_id: List[str]) -> None:
    """Reconstruct mail from blob storage.

    Can also scan dead letter queues to find mail that needs to be reconstructed.

    \b
    Reconstruct mail in dead letters:
    $ victoria email reconstruct uksprod1 -o output_dir

    \b
    Reconstruct a specific transaction ID
    $ victoria email reconstruct useprod2 -id <guid> -o output_dir

    \b
    Reconstruct a specific transaction ID, anonymising contents
    $ victoria email reconstruct useprod4 -id <guid> -o output_dir --anon
    """
    ensure_mailtoil(cfg)
    reconstruct_mail.reconstruct(cfg.mail_toil, cluster, output,
                                 transaction_id, anon, cfg)


@root_cmd.command()
@click.argument("cluster", nargs=1, type=str)
@click.pass_obj
def replay(cfg: schemas.EmailConfig, cluster: str) -> None:
    """Replay mail in service bus dead letters.

    \b
    To replay mail from a cluster:
    $ victoria email replay uksprod1
    """
    ensure_mailtoil(cfg)
    replay_deadletters.replay(cfg.mail_toil, cluster, cfg)


@root_cmd.command()
@click.argument("cluster", nargs=1, type=str)
@click.option("-f",
              "--file",
              metavar="FILE",
              type=str,
              required=False,
              help="TXT file containing transaction IDs to replay.")
@click.option("-id",
              "--transaction-id",
              type=str,
              required=False,
              help="Transaction ID to replay.")
@click.option("-o",
              "--output",
              metavar="URL",
              type=str,
              required=True,
              help="The SMTP endpoint to replay mail to.")
@click.pass_obj
def recover(cfg: schemas.EmailConfig, cluster: str, file: str, transaction_id: str,
            output: str) -> None:
    """Replay mail from blob storage through SaaS.

    To be used in the event of a failure causing mail to be persisted to
    blob storage but not sent onwards from SMTP receiver - being lost into
    the void.

    \b
    Usage example:

    \b
    Replay mail from a file containing transaction ids
    $ victoria email recover uksprod -f tx-ids.txt -o localhost:25

    \b
    Replay mail from a specific transaction id
    $ victoria email recover uksprod -id txId -o localhost:25
    """
    ensure_mailtoil(cfg)
    recover_mail.recover(cfg.mail_toil, cluster, file, transaction_id,  output, cfg)


@root_cmd.command()
@click.argument("manifest", nargs=1, type=str)
def send(manifest: str) -> None:
    """Send mail specified by manifest files.

    For information about the manifest format, please see the README:
    https://github.com/glasswall-sre/victoria_email

    \b
    Usage example:
    $ victoria email send uksprod.yaml
    """
    loaded_manifest = send_mail.Manifest.load(manifest)
    send_mail.send_manifest(loaded_manifest)


# plugin entry point
plugin = Plugin(name="email",
                cli=root_cmd,
                config_schema=schemas.EmailConfigSchema())
