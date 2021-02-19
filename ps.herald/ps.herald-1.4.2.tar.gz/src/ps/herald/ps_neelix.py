import click
import datetime
import socket
import sys
import time
import traceback
from ps.basic import Config
from ps.herald import create_app, __version__
from ps.herald import database
from ps.herald.model import Log, HeartBeat

TEST_ONLY = True
VERBOSE = False

TEXT_OF_THE_NOTIFICATION_MESSAGE = """
Dear Madam/Sir, <br>
<br>
 Neelix found a misbehaviour while analyzing the log on %(hostname)s
 The misbehaviour is  on system_id [%(system_id_p)s].
<br>

 The cause of the trigger was: [%(cause_p)s], the firing
 rule was [%(value_p)s].
<br>

 This event will be inserted into the logging messages of
 system [%(system_id_p)s]
 as an ERROR Event - by neelix.
<br>

 Please consult the Deployment Monitor for further information.
<br>

 Regards
<br>
  Neelix

<br>
In case of questions ... contact  _EP-Produktionsstrecke .
<br>
"""


def react(system_id_p, cause_p, value_p, row_p):
    """
    - system_id_p  Name of the system for which we react
    - cause_p      Name of the cause e.g. PATTERN or AGE
    - value_p      Value of the cause
    - row_p     table-row of the logging table correlated to the event
    """

    global VERBOSE
    session = database.get_session()
    logger = Config.logger
    logger.debug(
        f"Neelix reacts {system_id_p} : {cause_p} {value_p}",
        extra={"package_version": __version__},
    )
    mail_to = ""
    for name, value in Config.config_parser.items(system_id_p):
        if name == "mail_to":
            mail_to = value.split(",")
    if mail_to == "":
        mail_to = [Config.l_admin_mail]
    # message = message.message
    hostname = socket.gethostname()
    Config.send_a_mail(
        f"neelix@{hostname}",
        mail_to,
        f"neelix  {system_id_p}  {cause_p}",
        TEXT_OF_THE_NOTIFICATION_MESSAGE % (locals()),
        # logger_p = logger,
    )
    message = f"Neelix added Notification {cause_p} for {system_id_p}"
    row = Log(
        system_id=system_id_p,
        message=message,
        levelno=30,
        created=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    session.add(row)
    logger.debug(
        f"neelix react added new log entry {str(row)} ",
        extra={"package_version": __version__},
    )
    session.commit()


def notify(system_id_p, starting_at_p, till_p):
    global TEST_ONLY

    if system_id_p not in Config.config_parser.sections():
        return
    session = database.get_session()
    logger = Config.logger
    msg_pattern = "Not defined yet"
    allowed_age = 9999999999999999999999999
    logger.debug(
        "notify: check %s from %s to %s "
        % (system_id_p, starting_at_p, till_p),
        extra={"package_version": __version__},
    )
    for name, value in Config.config_parser.items(system_id_p):
        if name == "msg":
            msg_pattern = value
        if name == "age":
            allowed_age = eval(value)
    try:
        rows = (
            session.query(Log)
            .filter(
                Log.created >= starting_at_p,
                Log.created < till_p,
                Log.system_id == system_id_p,
            )
            .all()
        )

        #
        # Check the MSG content filter
        #
        for row in rows:
            if msg_pattern in str(row.message):
                logger.debug(
                    "For %s found a PATTERN Log Entry %s " % (str(row)),
                    extra={"package_version": __version__},
                )
                react(system_id_p, "PATTERN FOUND", "msg_pattern", row)
        #
        # Check the age filter
        #
        newest = (
            session.query(Log)
            .filter(Log.system_id == system_id_p)
            .order_by(Log.created.desc())
            .first()
        )
        try:
            # time_created = time.strptime(
            #    newest.created, "%Y-%m-%d %H:%M:%S.%f"
            # )
            seconds_newest = time.mktime(
                time.strptime(newest.created, "%Y-%m-%d %H:%M:%S.%f")
            )
            seconds_now = time.mktime(
                time.strptime(str(till_p), "%Y-%m-%d %H:%M:%S.%f")
            )
        except Exception:  # noqa: F841
            # time_created = time.strptime(
            #    newest.created, "%Y-%m-%d %H:%M:%S")  # noqa: F841
            seconds_newest = time.mktime(
                time.strptime(newest.created, "%Y-%m-%d %H:%M:%S")
            )
            seconds_now = time.mktime(
                time.strptime(str(till_p), "%Y-%m-%d %H:%M:%S.%f")
            )

        real_age = seconds_now - seconds_newest
        logger.debug(
            f"For {system_id_p} the last log message is aged {real_age}\
                 seconds: allowed are {allowed_age}  seconds",
            extra={"package_version": __version__},
        )

        if allowed_age < (seconds_now - seconds_newest):
            logger.debug(
                f"For {system_id_p} found an AGE Log Entry {str(newest)}",
                extra={"package_version": __version__},
            )
            react(system_id_p, "SYSTEM HEARTBEAT FAILURE", "age", newest)
        if TEST_ONLY:
            if system_id_p == "neelix":
                react(system_id_p, "HURZ", "test", newest)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logger.exception(
            "Exception in notify",
            extra={"package_version": __version__},
        )
        session.rollback()


def check():
    """[summary]

    Go through the systemid's found in the database:
       - check if somebody needs notification
       - update the hearbeat of the  systemid
    """
    initial_heart_beat_date = "0000-01-01 14:05:39"
    NOW = datetime.datetime.now()
    session = database.get_session()
    logger = Config.logger
    logger.debug(
        "Called",
        extra={"package_version": __version__},
    )
    try:
        rows = session.query(Log.system_id).distinct().all()
        for row in rows:
            system_id = row[0]
            print(f"SYSTEM_ID: {system_id}")
            if system_id == "None":
                continue
            try:
                old_heartbeat_entry = (
                    session.query(HeartBeat)
                    .filter(HeartBeat.system_id == system_id)
                    .all()[0]
                )
                newest_heartbeat = old_heartbeat_entry.newest_heartbeat
            except Exception:
                newest_heartbeat = initial_heart_beat_date
            notify(system_id, newest_heartbeat, NOW)
            try:
                session.query(HeartBeat).filter(
                    HeartBeat.system_id == system_id
                ).delete()
                row = HeartBeat(system_id=system_id, newest_heartbeat=NOW)
                session.add(row)
                session.commit()
            except Exception:
                logger.exception(
                    "Exception in check - rollback session",
                    extra={"package_version": __version__},
                )
                traceback.print_exc(file=sys.stdout)
                session.rollback()
                print("Except update")

    except Exception:
        traceback.print_exc(file=sys.stdout)
        logger.exception(
            "Exception in check - rollback session",
            extra={"package_version": __version__},
        )
        session.rollback()


@click.command()
@click.option(
    "--extra",
    "-x",
    is_flag=True,
    type=bool,
    default=False,
    help="internal tests only",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    type=bool,
    default=False,
    help="set verbose mode",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    type=bool,
    default=False,
    help="set debug mode",
)
@click.option(
    "--test_only", "-t", is_flag=True, help="print only what would be done"
)
def main(verbose, debug, extra, test_only):
    """
       Neelix scans the log and triggers actions.

     It's work is based on two models:\n
        - Log\n
        - HeartBeat\n

     First it  analyses the Log-model, which Log.system-id's are available.
     For each system_id, the log is analyzed, if "reactions" should
     be triggered.

     Reactions   are defined in the configuration File.

     Each system_id has it's own configuration section.

     Within each section currently two values could be defined:

          - MSG\n
          - AGE\n

     If either of these values is defined a parameter "MAIL_TO"
     has to be defined. Tho these addresses (a comma seperated list of
     email recipients Emails will be sent - alerting the error.
     e.g: \n
     \n
       [ch2eu] \n
          MAIL_TO=hedwig@company.ch,fried@h-l.com \n
          MSG="If this text would be found a message would be send." \n
          #AGE Value is given in seconds \n
          AGE=60*60*2 \n
       [hu2hu] \n
          MAIL_TO=hedwig@company.ch,fried@haufe-lexware.com \n
          #AGE Value is given in seconds \n
          AGE=60*60*2 \n
      \n
     Would consider the only logging-messages from the system-is's ch2eu \n
     and hu2hu. No other system_id
     will  be analyzed. Reactions will be triggered, if: \n
    \n
            - either we did not see a log message for the last 2 \n
              hours in the two systems \n
            - or in the ch2eu a logging msg appeared having a text \n
              like MSG " \n
    \n
    """
    global TEST_ONLY
    TEST_ONLY = test_only

    click.echo("ps_neelix. Debug mode is %s" % ("on" if debug else "off"))
    if extra:
        return 0
    app = create_app("ps_neelix", have_config_file=True)
    Config.logger.debug(
        "ps_neelix started", extra={"package_version": __version__}
    )
    Config.log_config_data()
    with app.app_context():
        check()


if __name__ == "__main__":
    sys.exit(main())
