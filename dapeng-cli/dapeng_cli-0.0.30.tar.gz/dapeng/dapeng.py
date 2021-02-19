from __future__ import print_function
import os
import re
import uuid
import pika
import socket
import json
import threading
import time
import shutil
import logging
import click
import requests
from junit_xml import TestSuite, TestCase

from .util import upload_file
from .version import VERSION
from .dapeng_api import DapengAPI, JobNotExists
from .settings import BROKER_SERVER_URL

LOGGER = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.ERROR)

UNIQUE_ID = uuid.uuid4()
QUEUE_NAME = "dapeng-cli.{}.{}".format(socket.gethostname(), UNIQUE_ID)


class TestcaseCheckThread(threading.Thread):
    """Background thread to periodly check tasks status.
    Default interval 60 seconds.
    """
    def __init__(self, case_id, channel, sleep_interval=60):
        super(TestcaseCheckThread, self).__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self.case_id = case_id
        self.channel = channel
        self.max_loop = 60 * 6

    def run(self):
        cnt = 0
        while True:
            case_info = DapengAPI.get_testcase(self.case_id)
            cnt += 1
            if cnt >= self.max_loop:
                LOGGER.error("Exceed max timeout: %s, exit!", (self.max_loop * self._interval))
                if self.channel:
                    self.channel.stop_consuming()
                break

            if not case_info:
                continue

            status = case_info['status'].lower()
            LOGGER.debug("checker[%s/%s], %s", cnt, self.max_loop, status)
            if status == 'finished':
                LOGGER.info("Test execution [Finish]")
                if self.channel:
                    self.channel.stop_consuming()
                    break

            # If no kill signal is set, sleep for the interval,
            # If kill signal comes in while sleeping, immediately
            #  wake up and handle
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break

    def kill(self):
        self._kill.set()

class JobListener(object):
    """Listen job status and logs"""

    def __init__(self, job_id, case_id=None, sync_log=True):
        self.job_id = job_id
        self.case_id = case_id
        self.channel = None
        self.connection = None
        self.consumer_tag = None
        self.case_info = None
        self.checker = None
        self.start_checker = True
        self.sync_log = sync_log
        self._logs = list()

    @property
    def logs(self):
        return "".join(self._logs)

    def _connect_broker(self):
        LOGGER.debug("start to connect to broker")
        binding_key = "*.%s" % self.case_id
        params = pika.URLParameters(BROKER_SERVER_URL)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # declare msg queue for current consumer
        self.channel.queue_declare(QUEUE_NAME, auto_delete=True)
        # bind to dapeng state exchange
        self.channel.queue_bind(
            exchange=DapengAPI.DAPENG_STATE_EXCHANGE,
            queue=QUEUE_NAME,
            routing_key=binding_key)

        if self.sync_log:
            # declare log exchange
            self.channel.exchange_declare(
                exchange=DapengAPI.DAPENG_LOG_EXCHANGE,
                exchange_type='topic')
            # bind to dapeng log exchange
            self.channel.queue_bind(
                exchange=DapengAPI.DAPENG_LOG_EXCHANGE,
                queue=QUEUE_NAME,
                routing_key=binding_key)

        LOGGER.debug("connected!")

    def do_query(self):
        if self.job_id and not self.case_id:
            LOGGER.debug("query case id")
            job_info = DapengAPI.get_job(self.job_id, True)
            if 'details' in job_info:
                self.case_id = job_info["details"][0]["id"]
            else:
                self.case_id = job_info["detail"][0]["id"]

        assert self.case_id
        self.case_info = DapengAPI.get_testcase(self.case_id)

    def _do_work(self, ch, method, properties, body):
        # handle task status and result
        if method.routing_key.startswith("state"):
            data = json.loads(body)
            status = data.get("status")
            if status:
                status = DapengAPI.DAPENG_TASK_STATUS.get(int(status)).lower()
                self.case_info["status"] = status
                LOGGER.info(" => Task is %s", self.status)

            self.case_info["runresult"] = data.get("result_text")
            LOGGER.debug('Conmuer result: %s', self.case_info["runresult"])

            if self.status == "finished" and self.case_info.get("runresult"):
                ch.stop_consuming()
        else:
            text = body.decode()
            self._logs.append(text)
            LOGGER.info(text) # print logs

    def start_listen(self):
        self.do_query()
        if self.status == "finished":
            LOGGER.debug("job is finised, won't connect!")
            return

        self._connect_broker()
        if not self.connection:
            return

        LOGGER.info('\n------------ Start Listener. To stop test press CTRL+C ------------')
        if self.status:
            LOGGER.info(" => Task is %s", self.status)

        if self.start_checker:
            self.checker = TestcaseCheckThread(self.case_id, self.channel)
            self.checker.start()

        self.consumer_tag = self.channel.basic_consume(
            queue=QUEUE_NAME, on_message_callback=self._do_work, auto_ack=True)
        self.channel.start_consuming()

    def force_quit(self):
        if self.channel:
            self.channel.stop_consuming()
        try:
            self.do_query()
            if self.status != "finished":
                DapengAPI.stop_job(self.job_id)
        except JobNotExists:
            pass

    @property
    def test_result(self):
        if self.status != "finished":
            self.do_query()
        return self.case_info["runresult"]

    @property
    def status(self):
        if self.case_info:
            status = self.case_info['status'].lower()
            return status
        return ""

    def close(self):
        if self.checker:
            LOGGER.debug("cancel checker")
            self.checker.kill()

        if self.channel:
            LOGGER.debug("close connection")
            self.channel.basic_cancel(self.consumer_tag)
            # self.channel.queue_delete(QUEUE_NAME)
            self.channel.close()


def create_dapeng_job(job_config=None, **kwargs):
    job_info = dict()
    image_file = kwargs.get("file")
    if image_file and os.path.exists(image_file):
        image_url = upload_file(kwargs.get("board"), image_file)
    else:
        image_url = image_file

    job_info['image_url'] = image_url
    LOGGER.info("Start to submit job.")
    if not job_config:
        job_config = {
            "header": {
                "version": 'v1.1',
                "suite": kwargs.get("suite"),
                "priority": kwargs.get("priority"),
                "isonthefly": True,
                "routing": kwargs.get("routing"),
                "runaccesstokenlist": kwargs.get("tokens"),
                "app_data_version": kwargs.get("app_data"),
                "job_id": kwargs.get("exist_job"),
                'max_rerun': kwargs.get("max_rerun_times")
            },
            "detail": [
                {
                    "name": kwargs.get("appname"),
                    "compiler": kwargs.get("compiler"),
                    "platform": kwargs.get("board"),
                    "target": kwargs.get("target"),
                    "bin": image_url,
                    "category": kwargs.get("category"),
                    'runtimeout': kwargs.get("timeout")
                }
            ]
        }
    if "name" not in job_config["header"]:
        job_config["header"]["name"] = str(UNIQUE_ID)
    LOGGER.info(json.dumps(job_config['detail'][0], indent=2))
    job_id, job_url = DapengAPI.submit_job(job_config)
    job_lis = JobListener(job_id, sync_log=kwargs.get("sync_log", True))
    job_info['job_url'] = job_url
    try:
        job_lis.start_listen()
    except KeyboardInterrupt:
        job_lis.force_quit()
    finally:
        job_lis.close()

    result = job_lis.test_result
    text = "=========== Test result: %s ===========" % result

    is_passed = False
    if result in ("Pass", "Semi Auto Pass"):
        click.secho(text, fg="green")
        is_passed = True
    else:
        click.secho(text, fg="red")
    job_info['result'] = result
    job_info['job_id'] = job_id
    job_info['logs'] = job_lis.logs
    return is_passed, job_info


@click.group(invoke_without_command=True)
@click.option('-log', type=click.Path(), help='log console output to file')
@click.option('--debug', is_flag=True, help='enable debug level')
@click.pass_context
def main(ctx, log, debug):
    if debug:
        level = logging.DEBUG
        format = "debug: %(message)s"
    else:
        level = logging.INFO
        format = "%(message)s"

    logging.basicConfig(level=level, format=format)
    # enable file logging
    if log:
        fh = logging.FileHandler(log)
        fh.setLevel(level)
        LOGGER.addHandler(fh)
    LOGGER.info("Dapeng CLI [Version: %s]\n", VERSION)


@main.command(help="rerun dapeng task")
@click.option('-id', prompt='case id', help='case id')
# @click.option('-a', '--app_data', help='set branch for app_data')
def rerun(id):
    case_info = DapengAPI.get_testcase(id)
    job_id = case_info["campaign_id"]
    DapengAPI.rerun_testcase(job_id, id)
    job_lis = JobListener(job_id, id)
    job_lis.start_checker = False
    try:
        time.sleep(3)
        job_lis.start_listen()
    except KeyboardInterrupt:
        job_lis.force_quit()
    finally:
        job_lis.close()

    result = job_lis.test_result
    text = "=========== Test result: %s ===========" % result
    if result == "Pass":
        click.secho(text, fg="green")
        exit(0)
    else:
        click.secho(text, fg="red")
        exit(1)

@main.command(help="verify dapeng tasks")
@click.option('-id', prompt='case id', help='case id')
@click.option('-a', '--app_data', help='set branch for app_data')
@click.option('-c', '--compiler', help='overried compiler to search, only work with --search')
@click.option('-t', '--target', help='overried target to search, only work with --search')
@click.option("--reserve/--no-reserve", default=True, help='search reserved jobs, only work with --search')
@click.option('--search', is_flag=True, help="search last passed result according the given case")
@click.option('-dpserver', default="prod1", help='dapeng instance: prod1/prod2/stage.')
def verify(id, app_data, compiler, target, reserve, search, dpserver):
    DapengAPI.setup_instance(dpserver)
    taskinfo = DapengAPI.get_testcase(id)
    if not taskinfo:
        click.secho("invalid task id")
        exit(1)

    if not search:
        click.echo("Verify case: %s" % id)
    else:
        params_to_query = {
            "compiler": taskinfo["compiler"],
            "platform": taskinfo["platform"],
            "target": taskinfo["target"],
            "testcase": taskinfo["test_case"],
            "id": id
        }

        if compiler:
            params_to_query["compiler"] = compiler

        if target:
            params_to_query["target"] = target

        if reserve:
            params_to_query["reserved"] = 'true'

        taskinfo = DapengAPI.get_testcase(id, params_to_query)
        if not taskinfo:
            click.secho("Not found last successful run!", fg="red")
            exit(1)

        click.secho("Found last successful run: {}.".format(taskinfo["id"]), fg="bright_blue")
        click.secho("  date:     %s" % taskinfo['runstarttime'])
        click.secho("  link:     http://dapeng/dapeng/information/requestdetail/{}/".format(taskinfo["id"]))
        click.secho("  source:   %s" % taskinfo["branch"])
        click.secho("  project:  %s" % taskinfo["project"])
        print("-----------------------------------")

    if taskinfo["bin"] in (None, "none", ""):
        click.secho("Invalid Task binary, please check your task", fg="red")
        exit(1)

    job_config = {
        "header": {
            "suite": taskinfo.get('test_type', "ksdk"),
            "priority": 3,
            "isonthefly": True,
            "routing": True,
            "runaccesstokenlist": "TEST_RUN,TEST_RUN_68,TEST_RUN_72,TEST_RUN_654",
        },
        "detail": [
            {
                "name": taskinfo["test_case"],
                "compiler": taskinfo["compiler"],
                "platform": taskinfo["platform"],
                "target": taskinfo["target"],
                "bin": taskinfo["bin"],
                "category": taskinfo.get("category", ''),
            }
        ]
    }
    if not app_data:
        app_data = taskinfo.get('version')

    if app_data:
        click.secho("AppData Branch:  %s" % app_data)
        job_config["header"]["app_data_version"] = app_data

    is_passed, _ = create_dapeng_job(job_config=job_config)
    if not is_passed:
        exit(1)


def validate_file_option(ctx, param, value):
    if value.startswith('http://') or value.startswith('ftp://'):
        pass
    elif not os.path.exists(value):
        raise click.BadParameter('File does not exists![%s]' % value)
    return value

@main.command(help="run a test on remote")
@click.option(
    '-f', '--file', callback=validate_file_option,
    required=True, help="image file, local file or file link")
@click.option('-b', '--board', required=True, help="board name")
@click.option('-n', '--appname', default="hello_world", help="app name")
@click.option('-c', '--compiler', default="armgcc", help="compiler name")
@click.option(
    '-t', '--target', default="release",
    help="app project target: debug/release")
@click.option(
    '-P', '--priority', default=3, type=click.IntRange(1, 6),
    help="task priority")
@click.option('-S', '--suite',
              default='ksdk',
              type=click.Choice(['ksdk', 'zephyr_test']),
              help="suite name, default ksdk")
@click.option(
    '-C', '--category', default="",
    help="sdk category[optionial], like demo_apps, driver_example")
@click.option(
    "-A", "--app_data", default="dev",
    help="set branch for app_data")
@click.option(
    "-T", "--tokens",
    default="TEST_RUN,TEST_RUN_68,TEST_RUN_72,TEST_RUN_654,TEST_RUN_A1,TEST_RUN_NPW",
    help="board tokens")
@click.option(
    '--routing/--no-routing', default=True,
    help="use case routing policy")
@click.option(
    "-timeout",
    help="set job timeout in seconds, default 12minutes", default=12 * 60)
@click.option(
    "--sync-log/--no-sync-log", default=True,
    help="sync remote logs in time")
@click.option(
    "-repeat-times", default=1, type=click.IntRange(1, ),
    help="times to repeat the test, useful for stress testing")
@click.option(
    "-max-rerun-times", default=1, type=click.IntRange(1, ),
    help="stop the test unitil result is passed or reach max rerun times")
@click.option(
    "--junitxml",
    help="generate junit xml report to specific file")
@click.option(
    '-dpserver', default="prod1",
    help='dapeng instance: prod1/prod2/stage.')
def test(file, board, appname, compiler, target, priority, suite,
         category, app_data, tokens, routing, timeout, sync_log, repeat_times, max_rerun_times, junitxml, dpserver):
    DapengAPI.setup_instance(dpserver)

    job_config = {
        'board': board,
        'compiler': compiler,
        'target': target,
        'appname': appname,
        'file': file,
        'routing': routing,
        'priority': priority,
        'suite': suite,
        'category': category,
        'app_data': app_data,
        'tokens': tokens,
        'timeout': timeout,
        'sync_log': sync_log,
        'max_rerun_times': max_rerun_times,
        'exist_job': None
    }

    results = list()
    test_cases = list()

    for t in range(repeat_times):
        start = time.time()
        is_passed, job_info = create_dapeng_job(**job_config)
        duration = time.time() - start
        results.append(is_passed)
        testcase = TestCase(job_config['appname'], job_config['appname'],
            duration, url=job_info['job_url'],
            category=category,
            log=job_info['logs'])

        if not is_passed:
            testcase.add_failure_info(job_info['result'])

        test_cases.append(testcase)
        if job_info and repeat_times > 1:
            # append tasks to exist job
            job_config['exist_job'] = job_info.get('job_id')
            # avoid re-upload file
            if job_info.get('image_url'):
                job_config['file'] = job_info.get('image_url')

    if junitxml:
        ts = TestSuite(suite, test_cases)
        with open(junitxml, 'w') as f:
            TestSuite.to_file(f, [ts], prettyprint=False)

    if all(results):
        exit(0)
    else:
        exit(1)

@main.command(help="create new jobs on Dapeng")
@click.option('-j', '--jsonfile', required=True, type=click.Path(exists=True), help="Use a JSON config file")
@click.option('-dpserver', default="prod1", help='dapeng instance: production/stage.')
def new(jsonfile, dpserver):
    DapengAPI.setup_instance(dpserver)
    with open(jsonfile) as fobj:
        job_config = json.load(fobj)
    DapengAPI.submit_job(job_config)


def _download(url, local_dir):
    local_filename = None
    with requests.get(url, stream=True) as r:
        fname = ''
        if "Content-Disposition" in r.headers.keys():
            fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
        else:
            fname = url.split("/")[-1]
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        local_filename = os.path.join(local_dir, fname)
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename

@main.command(help="download images to local")
@click.option('-id', required=True, help="job id")
@click.option('-d', '--download-dir', type=click.Path(exists=True), help="directory to download")
@click.option('-c', "--compiler", help="filter toolchain", multiple=True)
@click.option('-t', '--target', default="release", help="filter app target", multiple=True)
@click.option('-dpserver', default="prod1", help='dapeng instance: prod1/prod2/stage.')
def download(id, download_dir, compiler, target, dpserver):
    DapengAPI.setup_instance(dpserver)
    click.echo('Quering job %s on Dapeng server' % id)
    job_info = DapengAPI.get_job(id, True)
    selected_tasks = job_info['detail']

    if compiler:
        tasks = list()
        compiler = list(compiler)
        for task_info in selected_tasks:
            task_compiler = task_info.get('compiler')
            if task_compiler in compiler:
                tasks.append(task_info)

    if target:
        tasks = list()
        target = list(target)
        for task_info in selected_tasks:
            task_target = task_info.get('target')
            if task_target in target:
                tasks.append(task_info)
    else:
        selected_tasks = job_info['detail']

    total_cases = len(job_info['detail'])
    click.echo("Job name: %s" % job_info['header']['name'])
    click.echo("Total cases: %d" % total_cases)

    import concurrent.futures
    futures = list()
    invalid_urls = list()
    download_failed = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for task in selected_tasks:
            url = task.get('bin')
            if not url.startswith('http'):
                invalid_urls.append(task['id'])
                continue
            local_dir = os.path.join(download_dir, "{platform}/{category}/{testcase}/{compiler}/{target}/".format(**task))
            futures.append(executor.submit(_download, url, local_dir))

        total_futures = len(futures)
        with click.progressbar(
            concurrent.futures.as_completed(futures),
            label='downloading',
            length=total_futures) as bar:
            for future in bar:
                try:
                    future.result()
                except Exception as e:
                    download_failed.append(str(e))

        click.echo('Download directory: %s' % os.path.abspath(download_dir))
        if total_futures == len(selected_tasks):
            click.echo('Completed!')
        else:
            if invalid_urls:
                click.echo("invalid urls: %d" % len(invalid_urls))
            if download_failed:
                click.echo("download failed: %d" % len(download_failed))
            exit(1)

if __name__ == "__main__":
    main()
