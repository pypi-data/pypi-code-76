__doc__ = """ The Config Module delivers the *Basis* for Systems in the Production
     Systems world."""

import logging
import logging.handlers
import os
import signal
import sys
import tempfile
import time
import traceback
from configparser import (
    ConfigParser,
    NoOptionError,
    NoSectionError,
    ParsingError,
)
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import email.encoders

from socket import gethostname
from subprocess import PIPE, Popen

from ps.basic import DEV_STAGES, __version__, hms_string
from ps.basic.Patterns import LOGGING_PATTERNS, PATTERN_LANGUAGES

not_yet_defined = "not_yet_defined"


service_name = not_yet_defined
suffix = not_yet_defined
logging_port = not_yet_defined
logging_bridge_port = not_yet_defined
webserver_port = not_yet_defined
logging_level = not_yet_defined
log_file_name = not_yet_defined
logger = not_yet_defined
config_file_name = not_yet_defined
config_parser = not_yet_defined
dev_stage = not_yet_defined
herald_sqlite_filename = not_yet_defined
primary_herald_url = not_yet_defined
lock_file_name = not_yet_defined
admin_mail = not_yet_defined
curr_mail_sender = not_yet_defined
curr_mail_recipients = not_yet_defined
curr_mail_subject = not_yet_defined
curr_mail_text = not_yet_defined
is_testing = not_yet_defined
i_have_lock = False


import ps
import logging
import os
from importlib import reload

def reset_singleton(remove_log_file=True):
    """Reset the singleton's state initial values while testing."""
    if remove_log_file:
        if os.path.isfile(ps.basic.Config.log_file_name):
            os.remove(ps.basic.Config.log_file_name)
    Config = reload(ps.basic.Config)  # noqa: N806
    Config.Basic._instance = None
    properties = [ 
        "service_name",
        "suffix",
        "logging_port",
        "logging_bridge_port",
        "logging_level",
        "log_file_name",
        "logger",
        "config_file_name",
        "config_parser",
        "dev_stage",
        "herald_sqlite_filename",
        "primary_herald_url",
        "lock_file_name",
        "curr_mail_sender",
        "curr_mail_recipients",
        "curr_mail_subject",
        "curr_mail_text",
    ]   
    for property in properties:
        assert Config.__dict__["%s" % (property)] == "not_yet_defined"
    logging.shutdown()
    reload(logging)




MAX_SIZE_FOR_A_ROTATING_LOGFILE = 2000000
MAX_NUMBER_OF_OLD_ROTATING_LOGFILES = 10
PATTERN_LANGUAGE = "EN"


def sighup_handler(signum: int, frame):
    """[summary]
    On receipt of signal SIGHUP the configuration file will be read again
    updating it's data - accessible by the application
    via ps.basic.Config.config_parser.py.
 
    :param signum: [signal number SIGHUP only]
    :type signum: int
    :param frame: [description]
    :type frame: [type]
    :raises ForbiddenInitialisationOfSingleton: [description]
    """
    global config_parser, logger
    assert signum == signal.SIGHUP
    if config_parser != not_yet_defined:
        logger.debug(
            "SIGHUP Received. Print Configuration.",
            extra={"package_version": __version__},
        )
        #log_config_data(config_parser, logger)
        log_config_data()
    else:
        raise ForbiddenInitialisationOfSingleton(
            "SIGHUP called but module not yet initiated"
        )


# Enable the signal handler
signal.signal(signal.SIGHUP, sighup_handler)


def get_logging_data():
    """Provide the content of the current logfile."""
    global  log_file_name, logger
    if log_file_name == not_yet_defined:
         raise SingletonNotInitialized(
                    f"Unable to read the log file as it is not defined"
         )
    logging_data = ""
    try:
        with open(log_file_name,"r") as fp:
            logging_data = fp.read()
    except:
            logger.exception(
                f"Error reading log File {log_file_name}  version {__version__}" 
            )
     
    return logging_data
 

#def log_config_data(config_parser: ConfigParser, logger: logging.Logger):
def log_config_data():
    """[summary]

    :param config_parser: [description]
    :type config_parser: ConfigParser
    :param logger: [description]
    :type logger: logging.Logger
    """
    global config_parser, logger 
    html_string = "<table>"
    for section_name in config_parser.sections():
        html_string += "<tr><td>%s</td></tr>" % (section_name)
        for name, value in config_parser.items(section_name):
            html_string += "<tr><td>%s</td><td>%s</td></tr>" % (
                str(name),
                str(value),
            )
            #  name is lower() of the real name as default of config_parser
            if section_name == "GLOBAL" and name == "logging":
                numeric_level = getattr(logging, value.upper(), None)
                #                print(f"CONF2 Set Logging Level to {value}")
                logger.setLevel(numeric_level)
        html_string += "</table>"
        if html_string != "<table></table>":
            logger.debug(
                f"{html_string}", extra={"package_version": __version__}
            )


class Basic(object):
    """[summary]

    :param service_name_p: name of the service
    :type service_name_p: str
    :param have_config_file: [force usage of config file], defaults to False
    :type have_config_file: bool, optional
    :param guarded_by_lockfile: [create/check lockfile], defaults to False
    :type guarded_by_lockfile: bool, optional
    :param have_herald_url_in_config_file: [ force usage of \
        herald_url in config], defaults to False
    :type have_herald_url_in_config_file: bool, optional
    :raises ForbiddenInitialisationOfSingleton: [description]
    :raises ForbiddenInitialisationOfSingleton: [description]

    The Basic Class delivers the *Basis* for Systems in the Production System
    world.

       It enforces the same patterns for:
         - logging
         - configuration files
         - and maybe more

       throughout the different development stages.

       **Example Usage**

       >>> from ps.basic import Config
       >>> import os
       >>> project_name='ps'
       >>> dev_stage='DEVELOPMENT'
       >>> # DEV_STAGE has to be defined in the environment. Error else
       >>> os.environ["DEV_STAGE"]=dev_stage
       >>> # configuration files are built from the projects name
       >>> # and a shortcut for the development stage.
       >>> # They follow the ini syle (ms-world) for
       >>> # configuration files.
       >>> fp=open(os.path.join("/tmp", project_name + "_d.cfg"),"w")
       >>> written = fp.write("[GLOBAL]" + os.linesep)
       >>> written = fp.write("pattern_language=EN")
       >>> fp.close()
       >>> # you can set the directory, where config files live
       >>> os.environ["BASIC_CONFIGFILE_DIR"] = "/tmp"
       >>> singleton=Config.Basic(project_name,have_config_file = True)
       >>> Config.config_file_name
       '/tmp/ps_d.cfg'
       >>> assert(Config.config_file_name == "/tmp/ps_d.cfg")
       >>> my_version="0.0.alpha"
       >>> # Will leave an Info level log message in the local log file
       >>> # as in the (DEV_STAGE) central Log-Server/herald"
       >>> logger = Config.logger
       >>> logger.info("Hello LoggingWorld",
       ...      extra={"package_version":my_version})
       >>> # The application level access should occure via the
       >>> # provided class variables to read the config file
       >>> Config.config_parser.sections()
       ['GLOBAL']
       >>> Config.config_parser.items('GLOBAL')
       [('pattern_language', 'EN')]
       >>> # put logging messages to stdout too
       >>> singleton.verbose()

    """

    _instance = None

    def __init__(
        self,
        service_name_p: str,
        have_herald_url_in_config_file: bool = False,
        have_config_file: bool = False,
        guarded_by_lockfile: bool = False,
    ):
        """[summary]

        Create the singleton.
        """
        global service_name, dev_stage, suffix, logging_port
        global logging_bridge_port, webserver_port, logging_bridge_port
        global logging_level, log_file_name, logger, config_file_name
        global config_parser, herald_sqlite_filename, primary_herald_url
        global lock_file_name, admin_mail, curr_mail_sender
        global curr_mail_recipients, curr_mail_subject, curr_mail_text
        global is_testing, i_have_lock

        if Basic._instance is None:
            dev_stage = os.getenv("DEV_STAGE", None)
            if dev_stage is None or dev_stage not in DEV_STAGES.keys():
                raise ForbiddenInitialisationOfSingleton(
                    f"DEV_STAGE {dev_stage}  not an Allowed DEVELOPMENT STAGE"
                )
            Basic._instance = self
            service_name = service_name_p
            os.environ["SYSTEM_ID"] = service_name_p
            os.environ["SUB_SYSTEM_ID"] = gethostname()
            suffix = DEV_STAGES[dev_stage]["suffix"]
            log_file_name = os.path.join("LOG", service_name + suffix + ".log")
            logging_port = DEV_STAGES[dev_stage]["logging_port"]
            webserver_port = DEV_STAGES[dev_stage]["logging_port"] + 1
            logging_bridge_port = DEV_STAGES[dev_stage]["logging_bridge_port"]
            logging_level = DEV_STAGES[dev_stage]["logging_level"]
            admin_mail = DEV_STAGES[dev_stage]["l_admin_mail"]
            herald_sqlite_filename = os.path.join(
                os.getcwd(), f"herald.sqlite{suffix}"
            )
            primary_herald_url = ""
            lock_file_name = os.path.join(
                os.getcwd(), f"{service_name_p}_lock{suffix}"
            )
            is_testing = os.getenv("IS_TESTING", "NOT TESTING")

            # Create Local LOG Directory
            if not os.path.isdir("LOG"):
                try:
                    os.mkdir("LOG")
                except FileNotFoundError:  # pragma: no cover
                    sys.stderr.write(
                        f"Error creating LOG DIR in {os.getcwd()}: EXIT Now"
                    )
                    sys.stderr.write("Error creating LOG DIR: EXIT Now")
                    sys.exit(1)

            logger = logging.getLogger(service_name)
            my_filter = ContextFilter()
            logger.addFilter(my_filter)
            socket_handler = logging.handlers.SocketHandler(
                "localhost", logging_port
            )
            logger.addHandler(socket_handler)
            logfile_handler = logging.handlers.RotatingFileHandler(
                log_file_name,
                maxBytes=MAX_SIZE_FOR_A_ROTATING_LOGFILE,
                backupCount=MAX_NUMBER_OF_OLD_ROTATING_LOGFILES,
            )
            formatter = logging.Formatter(
                "%(asctime)s %(PRODUKT_ID)s %(SYSTEM_ID)s %(SUB_SYSTEM_ID)s\
                 %(SUB_SUB_SYSTEM_ID)s %(USER_SPEC_1)s %(USER_SPEC_2)s \
                 %(levelname)s %(name)-12s %(package_version)s \
                 %(lineno)d %(message)s"
            )
            logfile_handler.setFormatter(formatter)
            logger.addHandler(logfile_handler)

            logger.setLevel(logging_level)
            logger.debug(
                f"Logging initialized for pid {os.getpid()}",
                extra={"package_version": __version__},
            )

            if guarded_by_lockfile:
                self.__handle_lockfile__()
            if have_config_file:
                self.__handle_configfile__(have_herald_url_in_config_file)
        else:
            raise ForbiddenInitialisationOfSingleton(
                "Reinitialization of the singleton is not allowed"
            )

    def __handle_configfile__(self, have_herald_url_in_config_file: bool):
        """[summary]

        :param have_herald_url_in_config_file: [description]
        :type have_herald_url_in_config_file: bool
        :raises e: [description]
        :raises e: [description]
        :raises e: [description]
        :raises ForbiddenInitialisationOfSingleton: [description]
        """
        global config_parser, config_file_name, PATTERN_LANGUAGE
        global config_file_directory, primary_herald_url
        config_file_directory = os.getenv("BASIC_CONFIGFILE_DIR", False)
        if config_file_directory:
            if not os.path.isdir(config_file_directory):
                s = f"BASIC_CONFIGFILE_DIR {config_file_directory} not found."
                logger.fatal(
                    s,
                    extra={"package_version": __version__},
                )
                sys.stderr.write(s)
                raise ForbiddenInitialisationOfSingleton(s)
            else:
                config_file_name = os.path.join(
                    config_file_directory, service_name + suffix + ".cfg"
                )
                logger.info(
                    f"The config_file was forced  to {config_file_name}. ",
                    extra={"package_version": __version__},
                )
        else:
            config_file_name = os.path.join(
                os.getcwd(), service_name + suffix + ".cfg"
            )

        config_parser = ConfigParser()
        try:
            if os.path.isfile(config_file_name):
                config_parser.read(config_file_name)
            else:
                s = f"No config file {config_file_name} "
                s += "given, but it's usage is mandatory."
                logger.fatal(s, extra={"package_version": __version__})
                raise ForbiddenInitialisationOfSingleton(s)

        except (NoSectionError, ParsingError, NoOptionError) as e:
            e = sys.exc_info()[1]
            logger.exception(
                "Error reading config File: version %s" % (__version__)
            )
            sys.stderr.write("Error reading config File: EXIT Now")
            sys.stderr.write(traceback.format_exc())
            self.__exit__(1, 2, 3)
            if is_testing == "YES":
                raise e
            else:  # pragma: no cover
                raise e
                sys.exit(1)
        except SystemExit:  # pragma: no cover
            logger.exception(
                f"Error reading config File: version {__version__}"
            )
            e = sys.exc_info()[1]
            self.__exit__(1, 2, 3)
            raise e

        if have_herald_url_in_config_file:
            try:
                primary_herald_url = config_parser.get("GLOBAL", "herald_url")
            except (NoSectionError, ParsingError, NoOptionError):
                s = "Value of herald_url in GLOBAL section of "
                s += f"{config_file_name} not given - but needed. EXIT NOW"
                logger.fatal(
                    s,
                    extra={"package_version": __version__},
                )
                sys.stderr.write(s)
                raise ForbiddenInitialisationOfSingleton(s)
        try:
            PATTERN_LANGUAGE = config_parser.get("GLOBAL", "pattern_language")
            if PATTERN_LANGUAGE not in PATTERN_LANGUAGES:
                s = "Value of pattern_language in GLOBAL section of "
                s += f"{config_file_name}  not allowed. EXIT NOW"
                logger.fatal(
                    s,
                    extra={"package_version": __version__},
                )
                sys.stderr.write(s)
                raise ForbiddenInitialisationOfSingleton(s)
        except (NoSectionError, ParsingError, NoOptionError):
            PATTERN_LANGUAGE = "EN"
            d = {}
            d["PATTERN_LANGUAGE"] = PATTERN_LANGUAGE
            logger.debug(
                template_writer(
                    LOGGING_PATTERNS,
                    PATTERN_LANGUAGE,
                    "LANGUAGE_PATTERN_FAILED",
                    d,
                ),
                extra={"package_version": __version__},
            )

        # Call the modules sighup_handler which will write the configuration
        # data to the log
        #log_config_data(config_parser, logger)
        log_config_data()

    def __handle_lockfile__(self):
        """[summary]

        :raises LockedInitialisationOfSingleton: [description]
        :raises LockedInitialisationOfSingleton: [description]
        """
        global i_have_lock, logger, is_testing, lock_file_name

        def init_lockfile(fq_path_to_lockfile_p):
            fp = open(lock_file_name, "w")
            fp.write("%s" % os.getpid())
            fp.close()
            logger.info(
                f"system {service_name} lockfile {lock_file_name} created",
                extra={"package_version": __version__},
            )

        if not os.path.isfile(lock_file_name):
            try:
                init_lockfile(lock_file_name)
                i_have_lock = True
            except FileNotFoundError:  # pragma: no cover
                s = f"Error opening/writing lock File {lock_file_name}"
                s += f"EXIT Now version {__version__}"
                logger.exception(s)
                sys.stderr.write(s)
                sys.stderr.write(traceback.format_exc())
                sys.exit(1)
            logger.info(
                "system %s started new lock guarded instance on %s"
                % (service_name, lock_file_name),
                extra={"package_version": __version__},
            )
        else:
            with open(lock_file_name, "r") as fp:
                pid = fp.read().strip()
            st = os.stat(lock_file_name)
            age = hms_string(time.time() - st.st_mtime)
            s = f"{lock_file_name}  locked by process with pid "
            s += f"{pid}  for: {age} : version {__version__}"
            logger.info(s)
            try:
                os.kill(int(pid), 0)
                s = f"process with pid {pid} is still alive Exit now "
                logger.info(s, extra={"package_version": __version__})
                raise LockedInitialisationOfSingleton(s)
            except OSError:
                s = f"process with pid {pid} is not alive:\
                     Will Remove the lock file"
                logger.error(
                    s,
                    extra={"package_version": __version__},
                )
                sys.stderr.write(s)
                os.remove(lock_file_name)
                raise LockedInitialisationOfSingleton(s)

    def verbose(self):
        """[summary]

        Logging messages additionally will be sent to stderr.
        """
        global logger
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formater = logging.Formatter("%(asctime)s   %(lineno)d - %(message)s")
        ch.setFormatter(formater)
        logger.addHandler(ch)

    def __exit__(self, exc_type, exc_value, traceback):
        """[summary]

        :param exc_type: [description]
        :type exc_type: [type]
        :param exc_value: [description]
        :type exc_value: [type]
        :param traceback: [description]
        :type traceback: [type]
        """
        if exc_type == 1 and exc_value == 2 and traceback == 3:
            try:
                if os.path.isfile(lock_file_name):
                    logger.debug(
                        f"remove lock_file {lock_file_name}",
                        extra={"package_version": __version__},
                    )
                    os.unlink(lock_file_name)
            except FileNotFoundError:  # pragma: no cover
                s = f"ERR: remove lock_file: version {__version__}"
                logger.exception(s)
                sys.stdout.write(s)
                sys.stderr.write(s)
                sys.stderr.write(traceback.print_exc())
        else:  # pragma: no cover
            logger.error(
                "remove log_file Leave Singleton with nonstandard __exit__",
                extra={"package_version": __version__},
            )
            sys.stderr.write("Leave Singleton with nonstandard __exit__")

    def __del__(self):
        """Allow to use in with."""
        #        #pass
        #        # rudiments from python2 - seems to be not needed any longer
        if i_have_lock:
            self.__exit__(1, 2, 3)


class ContextFilter(logging.Filter):
    """[summary]

    Merges additional values into the logging message.

    :param logging: [description]
    :type logging: [type]
    :return: [description]
    :rtype: [type]
    """

    def filter(self, record):
        """[summary]

        Add additional field to a log message.

        :param record: [description]
        :type record: [type]
        :return: [description]
        :rtype: [type]
        """
        if "package_version" not in record.__dict__:
            record.package_version = "undef"
        record.SYSTEM_ID = os.getenv("SYSTEM_ID", "None")
        record.SUB_SYSTEM_ID = os.getenv("SUB_SYSTEM_ID", "None")
        record.SUB_SUB_SYSTEM_ID = os.getenv("SUB_SUB_SYSTEM_ID", "None")
        record.PRODUKT_ID = os.getenv("PRODUKT_ID", "None")
        record.USER_SPEC_1 = os.getenv("USER_SPEC_1", "None")
        record.USER_SPEC_2 = os.getenv("USER_SPEC_2", "None")
        return True


class SingletonNotInitialized(Exception):
    """Exception raised if a function is called which needs an initialized State

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, message: str):
        """Write a message.

        :param message: [description]
        :type message: [str]
        """
        self.message = message

class LockedInitialisationOfSingleton(Exception):
    """Exception raised if the start of a service finds an existing lockfile.

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, message: str):
        """Write a message.

        :param message: [description]
        :type message: [str]
        """
        self.message = message


class ForbiddenInitialisationOfSingleton(Exception):
    """Exception raised if the start of a Service is not possible.

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, message):
        """[summary]

        :param message: [description]
        :type message: [type]
        """
        self.message = message


def template_writer(
    patterns_p: dict, pattern_offset_p: dict, pattern_p: dict, d_vars_p: dict
):
    """

    Template writer used to generate strings based on the Pattern module.

    :param patterns_p: [description]
    :type patterns_p: dict
    :param pattern_offset_p: [description]
    :type pattern_offset_p: dict
    :param pattern_p: [description]
    :type pattern_p: dict
    :param d_vars_p: [description]
    :type d_vars_p: dict
    :raises KeyError: [description]
    :return: [description]
    :rtype: [type]
    """
    try:
        template = patterns_p[pattern_offset_p][pattern_p]
        return template % (d_vars_p)
    except KeyError:
        logger.exception(
            "unable to generate string in %s from template %s"
            % (pattern_offset_p, pattern_p)
        )
        raise KeyError(pattern_offset_p)


def ps_shell(cmd_p: str, env_p: dict = None):
    """
    Execute a command in a spawned Process.

    :param cmd_p: [cmd to be executed ]
    :type cmd_p: str
    :param env_p: [environment to use], defaults to None
    :type env_p: dict, optional
    :return: [(out, err, exit, time_needed)]
    :rtype: [tuple]
    """
    global logger, service_name
    success = "SUCCESS"
    start_time = time.time()
    child = Popen(
        cmd_p,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        env=env_p,
        universal_newlines=True,
    )
    (stdout, stderr) = child.communicate()
    exitcode = child.poll()
    end_time = time.time()

    time_needed = hms_string(end_time - start_time)
    if exitcode != 0:
        success = "ERROR"
    logger.debug(
        f"{success} {time_needed}  {cmd_p}",
        extra={"package_version": __version__},
    )
    if exitcode != 0:
        logger.error(
            "%d %s" % (int(exitcode), stderr),
            extra={"package_version": __version__},
        )

    return (
        str(stdout).strip().split("\n"),
        str(stderr).strip().split("\n"),
        exitcode,
        time_needed,
    )


def exec_interpreter_from_string(source_code: str):
    """Execute  a given python programm in a new spawned python interpreter.

    :param source_code: [python source code]
    :type source_code: str
    :return: [(out, err, exit, time_needed)]
    :rtype: [tuple]


    """
    tmp = tempfile.NamedTemporaryFile(mode="w+t")
    try:
        tmp.write(source_code)
        tmp.flush()
        cmd = f"{sys.executable}  {tmp.name}"
        out, err, exit, time_needed = ps_shell(cmd)
    finally:
        tmp.close()

    return out, err, exit, time_needed


def send_a_mail(sent_from:str , l_send_to_p:list, subject:str, text:str, files:list=[], serverstr="localhost", test_only:bool=False):
    assert isinstance(l_send_to_p, list)
    assert isinstance(files, list)
    global logger,curr_mail_recipients,curr_mail_sender,curr_mail_subject,curr_mail_text,dev_stage,__version__
   
    logger.debug(f"TRY send_mail FROM {sent_from}  TO {str(l_send_to_p)}   subject {subject}",extra={"package_version":__version__})

    msg = MIMEMultipart('alternative')
    msg['From'] = sent_from
    msg['To'] = COMMASPACE.join(l_send_to_p)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(text, 'html'))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        email.encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', 'attachment; filename="%s"' %
                                   os.path.basename(f))
        msg.attach(part)

    try:

        if not test_only and dev_stage != "TESTING" and not os.environ["TESTING"]:
                     smtp = smtplib.SMTP(server)
                     smtp.sendmail(sent_from, l_send_to_p, msg.as_string())
                     smtp.close()
        else:
                     curr_mail_sender      = sent_from
                     curr_mail_recipients  = l_send_to_p
                     curr_mail_subject     = subject
                     curr_mail_text        = text

        logger.debug(f"SUCC send_mail FROM {sent_from}  TO {str(l_send_to_p)}   subject {subject}",extra={"package_version":__version__})
    except:
        logger.debug(f"EXCEPTION send_mail FROM {sent_from}  TO {str(l_send_to_p)}   subject {subject}",exc_info=True, extra={"package_version":__version__})
        sys.stdout.write("Exception Sending Email")
        try:
            logger.debug("Try To send via shell mail", extra={"package_version":__version__})
            for dst in l_send_to_p:
                cmd = ' echo "%s" | mail -s "%s" %s' % (text, subject, dst)
                logger.debug("Try to send mail via shell {cmd}",extra={"package_version":__version__})
                o, e, ex, t = ps_shell(cmd)
                if int(ex) > 0:
                    logger.error("FAILURE Mail via shell",extra={"package_version":__version__})
                else:
                    logger.info("SUCCESS Mail via shell to {dst}",extra={"package_version":__version__})
        except:
           logger.debug(f"EXCEPTION send_mail via shell  FROM {sent_from}  TO {str(l_send_to_p)}   subject {subject}",exc_info=True, extra={"package_version":__version__})












