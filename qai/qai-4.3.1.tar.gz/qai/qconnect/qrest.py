import math
import multiprocessing
import os
import time
from pathlib import Path

from sanic import Sanic, response
from sanic.log import logger

from qai.funq import partial
from qai.issues.add_issues import (
    add_issues_format_insensitive,
    add_issues_format_insensitive_batch,
)
from qai.issues.logs import get_payload_stats
from qai.issues.validation import Validator
from qai.qconnect.qremoteconnection import QRemoteConnection
from qai.version import __version__


def get_cpu_quota_within_docker():
    """
    By default, we use mp.cpu_count()
    HOWEVER, if there are cpu limits in certain paths, we assume those are
    from k8s/docker and override with those values
    """
    cpu_cores = multiprocessing.cpu_count()

    cpu_shares = Path("/sys/fs/cgroup/cpu/cpu.shares")

    if cpu_shares.exists():
        with cpu_shares.open("rb") as r:
            request_cpu_shares = int(r.read().strip())
            cpu_cores = (
                math.ceil(request_cpu_shares / 1024)
                if request_cpu_shares > 0
                else multiprocessing.cpu_count()
            )
            print(
                f"CPU request limit: {round(request_cpu_shares / 1024, 2)}, will spin {cpu_cores} worker(s)."
            )
    else:
        print(f"CPU_shares not found, will spin {cpu_cores} worker(s).")
    return cpu_cores


async def post_root(self, request):
    json_data = request.json
    try:
        # if it has items it is a dict
        _ = json_data.items()
        # if it is a dict, make it an array
        els = [json_data]
    except AttributeError:
        # can't call .items(), so it's already an array
        els = json_data
    resp_list = []

    if self.batching:
        resp_list = add_issues_format_insensitive_batch(
            self, els, self.debug, verbose=self.verbose
        )
        return response.json(resp_list)

    for el in els:
        el = add_issues_format_insensitive(
            self, el, self.validator, debug=self.debug, verbose=self.verbose
        )
        resp_list.append(el)
    return response.json(resp_list)


async def get_root(self, request):
    try:
        white_lister = self.white_lister
    except AttributeError:
        white_lister = None
    resp_obj = {
        "service": self.category,
        "status": "up",
        "host": self.host,
        "port": self.port,
        "qai_version": __version__,
        "white_lister": str(white_lister),
        "analyzer": str(self.analyzer),
    }
    return response.json(resp_obj)


async def add_start_time(request):
    """Prepend initial time when this request was served."""
    request.ctx.start_time = time.time()


async def add_perf_stats(self, request, response):
    """
    Prepend initial time when this request was served.
    Log the access long on each request.
    Log num of segments, sentences, words in payload.
    Log sentence and word speed.
    """
    is_get = request.method.lower() == "get"
    is_check = request.path in ["/ready", "/healthy"]
    should_log = not (is_get or is_check)
    if should_log:
        latency = round((time.time() - request.ctx.start_time) * 1000)
        n_seg, n_sent, n_word = get_payload_stats(request.json, self.validator.nlp)
        latency_sec = latency / 1000

        try:
            # log how long it takes to process seg/sent
            seg_latency = round(latency_sec / n_seg, 2)
            sent_latency = round(latency_sec / n_sent, 2)

            # how many words per sec
            word_speed = round(n_word / latency_sec, 2)

        except:
            # markers - logging error
            seg_latency = -1
            sent_latency = -1
            word_speed = -1

        logger.info(
            (
                "{method} {url} {status} {latency}ms {reqbytes}reqBytes "
                "{resbytes}resBytes {n_seg}segs {n_sent}sents {n_word}words "
                "{seg_latency}spSeg {sent_latency}spSent {word_speed}wps"
            ).format(
                method=request.method,
                ip=request.ip,
                url=request.url,
                status=response.status,
                latency=latency,
                reqbytes=len(request.body),
                resbytes=len(response.body),
                n_seg=n_seg,
                n_sent=n_sent,
                n_word=n_word,
                seg_latency=seg_latency,
                sent_latency=sent_latency,
                word_speed=word_speed,
            )
        )


class QRest(QRemoteConnection):
    def __init__(
        self,
        analyzer,
        category="",
        white_lister=None,
        host="0.0.0.0",
        port=5000,
        workers=None,
        config_path=["conf", "config.json"],
        batching=False,
        debug=False,
        verbose=False,
        sentence_token_limit=1024,
        ignore_html=True,
        ignore_inside_quotes=False,
    ):
        self.host = host
        self.port = port

        config_file = os.path.join(os.getcwd(), *config_path)
        super().__init__(analyzer, category, white_lister, config_file)

        if workers is None:
            # get workers from configs
            try:
                self.workers = int(self.configs["WORKER_COUNT"])
                print(f"Found WORKER_COUNT in configs, setting it to {self.workers}")
            except KeyError:
                # WORKER_COUNT not in configs
                print(
                    "WORKER_COUNT not set in code or configs, using as many as CPU cores available"
                )
                self.workers = get_cpu_quota_within_docker()
                print(f"set WORKER_COUNT to {self.workers}")
                # Don't catch ValueError, as this happens when we can't coerce WORKER_COUNT to an int
                # in that case we should die and yell at the user..

        elif isinstance(workers, int):
            self.workers = workers
        else:
            raise ValueError(
                (
                    "QRest instantiated with invalid workers value. "
                    "Workers should be set via config, set to an integer value, or not set"
                )
            )
        self.batching = batching

        if self.batching == True and self.workers > 1:
            print("batching set to True - MUST have only 1 worker")
            old_worker_count = self.workers
            self.workers = 1
            print(f"reset workers from {old_worker_count} to {self.workers}")

        self.debug = debug
        self.verbose = verbose
        self.sentence_token_limit = sentence_token_limit
        self.ignore_html = ignore_html
        self.ignore_inside_quotes = ignore_inside_quotes
        nlp_obj = getattr(analyzer, "nlp", None)
        self.validator = Validator(
            nlp_obj=nlp_obj,
            sentence_token_limit=sentence_token_limit,
            ignore_html=ignore_html,
        )

        self.app = Sanic(__name__)

        # Add the request and response middleware
        self.app.request_middleware.append(add_start_time)
        unary_add_perf_stats = partial(add_perf_stats, self)
        self.app.response_middleware.append(unary_add_perf_stats)

        # Add routes
        # This works, but it is better to make these after instantiating the class
        # that way you don't need partial application... see README
        unary_post_root = partial(post_root, self)
        unary_get_root = partial(get_root, self)
        self.app.add_route(unary_post_root, "/", methods=["POST"])
        self.app.add_route(unary_get_root, "/", methods=["GET"])
        self.app.add_route(unary_get_root, "/ready", methods=["GET"])
        self.app.add_route(unary_get_root, "/healthy", methods=["GET"])

    def get_future(self):
        """
        Return a Future (Promise in JS land) that can be put on an event loop
        """
        return self.app.create_server(host=self.host, port=self.port)

    def connect(self):
        """
        Doesn't return, makes a blocking connection
        Only use if you are ONLY using REST
        This is a more robust REST server than get_future makes
        see:
        https://sanic.readthedocs.io/en/latest/sanic/deploying.html#asynchronous-support
        """
        if self.workers > 1:
            print(
                f"grpc, and hence AutoML, only support 1 worker, "
                + f"but you are using {self.workers}"
            )
        return self.app.run(
            host=self.host, access_log=False, port=self.port, workers=self.workers
        )
