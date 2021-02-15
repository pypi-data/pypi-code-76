# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:

"""Main module."""
import csv
import os
import time
import logging
import json
import asyncio
import aiohttp
import aiofiles

from dotmap import DotMap
from tqdm import tqdm

from . import cliargs
from .service import OliverAPI

from .utils import (convert_iso_datetime, die, words, getnpopn,
                    get_csv_non_empty_rows, limit_upload_rate)

from .settings import (MAX_POLLING_WINDOW, MAX_ASYNC_UPLOADS,
                       API_CONNECTION_TIMEOUT, REQUESTS_LIMIT_PERIOD_SECS,
                       MAX_REQUESTS_PER_SEC)


opts = {}


def get_results_for_pid_list_async(pid_file, output_dir, level="call"):
    """
    Collect asynchronously successfull results for all pids on file `pid_file`
    """
    failed_pids = []
    polling_pids = []
    noresult_pids = []

    service_api = OliverAPI(opts=opts)

    polling_window = min(MAX_POLLING_WINDOW, opts.polling)

    pending_pids = list(words(pid_file))

    with tqdm(total=len(pending_pids)) as pbar:

        polling_pids += getnpopn(pending_pids, polling_window - len(polling_pids))

        while len(pending_pids) > 0 or len(polling_pids):

            ready_processes, transient_pids, failed = service_api.getInfoAsync(polling_pids, poll=True)

            pending_pids += transient_pids
            failed_pids += failed

            for pid in list(ready_processes) + transient_pids + failed:
                polling_pids.remove(pid)

            if level == "call":
                noresult_pids = service_api.GetResultsAsync(ready_processes, output_dir=output_dir)
            elif level == "frames":
                noresult_pids = service_api.GetFrameResultsAsync(ready_processes, output_dir=output_dir)
            elif level == "asr":
                noresult_pids = service_api.GetASRResultsAsync(ready_processes, output_dir=output_dir)
            elif level == "features":
                noresult_pids = service_api.GetFeaturesResultsAsync(ready_processes, output_dir=output_dir)
            elif level == "diarization":
                noresult_pids = service_api.GetDiarizationResultsAsync(ready_processes, output_dir=output_dir)

            failed_pids += noresult_pids

            for pid in noresult_pids:
                ready_processes.pop(pid)

            polling_pids += getnpopn(pending_pids, polling_window - len(polling_pids))
            pbar.update(len(ready_processes) + len(noresult_pids))

    return failed_pids


def get_results_for_pid_list(pid_file, output_dir, level="call"):
    """
    Collect successfull results for all pids on file `pid_file`
    """
    missing_pids = []

    service = OliverAPI(opts=opts)

    # Iterate over all ids until they're all fetched or discarded
    pending_pids = list(words(pid_file))

    while len(pending_pids) > 0:
        pid = pending_pids.pop(0)

        resp = service.GetInfo(pid, poll=True)

        if not resp:
            logging.warning("Not found pid {}.".format(pid))
            missing_pids += [pid]
            continue

        if resp.status == 2:
            logging.debug("Processing status for pid {}: {}. Downloading results.".format(pid, resp.status))
            if level == "call":
                service.GetResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "frames":
                service.GetFrameResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "asr":
                service.GetASRResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "features":
                service.GetFeaturesResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "diarization":
                service.GetDiarizationResults(pid, output_dir=output_dir, dest=resp.source)
        elif resp.status == -1:
            logging.warning("Retrying job with pid: {}. Processing status: {}".format(pid, resp.status))
            pending_pids += [pid]
        else:
            logging.warning("Problem with pid: {}. Processing status: {}. Reason: {}".format(pid, resp.status, resp.statusmsg))
            missing_pids += [pid]

    return missing_pids

async def submit_from_csv_async(csv_file, pid_file, tag=None, nchannels=1, calldirection='1', max_async_sends=MAX_ASYNC_UPLOADS):

    api = OliverAPI(opts=opts)

    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': opts.apitoken
    }

    uploads_history = []
    tasks = []

    if not api.authorized():
        logging.warning("Not valid credentials provided")
        return

    non_empty_rows = get_csv_non_empty_rows(csv_file)

    with tqdm(total=non_empty_rows) as pbar:
        async with aiohttp.ClientSession(headers=headers, conn_timeout=API_CONNECTION_TIMEOUT) as session:
            async with aiofiles.open(pid_file, 'w') as pidsfile:
                with open(csv_file, 'r') as f:
                    reader = csv.reader(f, delimiter=",", quotechar="'")

                    sends = 0
                    for row in reader:
                        if not row:
                            logging.warning("Skipping empty lines included in '{}' file".format(csv_file))
                            continue

                        filepath, data = get_audio_metadata(row, tag, nchannels, calldirection)

                        if not filepath:
                            continue

                        tasks.append(
                            api.send_audio_async(session, pidsfile, filepath, os.path.basename(filepath), **data)
                        )

                        sends += 1

                        if sends < max_async_sends:
                            continue

                        if not uploads_history:
                            initial_time_called = time.monotonic()
                            uploads_history.append((initial_time_called, sends))

                        await asyncio.gather(*tasks)
                        tasks.clear()
                        pbar.update(sends)

                        last_time_called = time.monotonic()

                        if limit_upload_rate(uploads_history, last_time_called, sends):
                            await asyncio.sleep(REQUESTS_LIMIT_PERIOD_SECS)

                        sends = 0

                    await asyncio.gather(*tasks)
                    pbar.update(sends)


def submit_single_file(files, data):
    """
    Submit single audio file
    """
    service = OliverAPI(opts=opts)

    showRequest(data, files)
    response = service.send_audio(files, data)

    return response


def showRequest(data, files):
    """
    Log the resquest in logging.debug
    """
    logging.debug("sending a post request")
    logging.debug("\t %12s: %s", 'data', data)
    logging.debug("\t %12s: %s", 'files', files)


def showResponse(response):
    """
    Log the response in logging.debug
    """
    logging.debug('api response:')
    logging.debug('\t%12s: %s', 'status', response.status_code)
    logging.debug('\t%12s: %s', 'reason', response.reason)


def submit_single_file_no_params(file_name):
    # Default data values
    data = {'channels': '1', 'calldirection': '1'}
    try:
        files = {'file': open(file_name, 'rb')}
    except FileNotFoundError:
        logging.warning("File '{}' does not exist.".format(file_name))
        return ''

    return submit_single_file(files, data)


def submit_file_list(file_list):
    with open(file_list, 'r') as fl:
        for line in fl:
            file_name = line.rstrip()
            logging.debug('Submitting {}'.format(file_name))
            r = submit_single_file_no_params(file_name)
            logging.debug(r.url)
            logging.debug(r.text)


def submit_csv_file(csv_file, pid_file, tag=None, nchannels=1, calldirection='1'):

    n_failures = 0

    with open(csv_file, 'r') as f:
        with open(pid_file, 'w') as p:
            reader = csv.reader(f, delimiter=",", quotechar="'")
            for row in reader:
                if not row:
                    logging.warning("Skipping empty lines included in '{}' file".format(f))
                    continue

                try:
                    filename, data = get_audio_metadata(row, tag, nchannels, calldirection)
                except Exception as e:
                    logging.warning("Skipping line in '{}' csv file: {}".format(csv_file, e))
                    continue

                try:
                    files = {'file': open(filename, 'rb')}
                except FileNotFoundError:
                    logging.warning("Skipping line in '{}' file because '{}' file does not exist.".format(f, filename))
                    continue

                r = submit_single_file(files, data)

                if r.status_code != 200:
                    n_failures += 1
                else:
                    j = json.loads(r.text)
                    p.write("{}\n".format(j['pid']))

    return n_failures


def get_audio_metadata(row, tag, nchannels, calldirection):
    DATA_FIELDS = [
        'channels', 'calldirection', 'agentId', 'agentTeam', 'campaignId',
        'calltype', 'calltime', 'timezone', 'ANI', 'tag', 'meta',
        'predictionmode', 'tasks'
    ]

    data = {}

    filename = row[0]
    n_data_values = len(row)

    if n_data_values > 1:
        for idx, value in enumerate(row[1:]):
            if value:
                if DATA_FIELDS[idx] == 'channels':
                    value = int(value)
                elif DATA_FIELDS[idx] == 'calltime':
                    value = convert_iso_datetime(value)

                data[DATA_FIELDS[idx]] = value

                if DATA_FIELDS[idx] == 'tag':
                    if tag is not None:
                        data['tag'] += ',{}'.format(tag)

    # No ASR column at csv so default to asr=TRUE
    if 'predictionmode' not in data:
        data['predictionmode'] = 'full'

    if 'tag' not in data and tag is not None:
        data['tag'] = tag

    # Validate if number of channels is correct or set default
    if 'channels' not in data or data['channels'] not in (1, 2):
        data['channels'] = nchannels
        logging.warn('Setting value for channels to {} for audio {}'.format(nchannels, filename))

    # Validate if call direction is correct or set default
    if 'calldirection' not in data or data['calldirection'] not in ('1', '2'):
        data['calldirection'] = calldirection
        logging.warn('Set value for call direction to {} for audio {}'.format(calldirection, filename))

    return filename, data


def poll_for_results(args, level="call"):
    if not os.path.exists(args.resultsDir):
        logging.warning("Creating new folder: {}".format(args.resultsDir))
        os.makedirs(args.resultsDir)

    if args.asyncmode:
        missing_pids = get_results_for_pid_list_async(args.pidFile, args.resultsDir, level)
    else:
        missing_pids = get_results_for_pid_list(args.pidFile, args.resultsDir, level)

    if len(missing_pids) > 0:
        logging.warning("Not found {} results for the following processes: {}".format(level, missing_pids))
        return 1
    else:
        logging.info("Results for all pids have been downloaded.")
        return 0


def send_audio(args):
    logging.info('Using csv file: {}'.format(args.csvFile))

    if args.asyncmode:
        try:
            loop = asyncio.get_event_loop()

            loop.run_until_complete(submit_from_csv_async(
                args.csvFile, args.pidFile,
                tag=args.tag, nchannels=args.nchannels,
                max_async_sends=opts.uploads)
            )
        finally:
            loop.close()
            return 0

    else:
        n_failures = submit_csv_file(
            args.csvFile, args.pidFile, tag=args.tag, nchannels=args.nchannels
        )

        if n_failures == 0:
            logging.info("File uploading ran successfully.")
            return 0

    return 1


def get_results(args):
    return poll_for_results(args, level="call")


def get_results_frames(args):
    return poll_for_results(args, level="frames")


def get_results_asr(args):
    return poll_for_results(args, level="asr")


def get_results_features(args):
    return poll_for_results(args, level="features")


def get_results_diarization(args):
    return poll_for_results(args, level="diarization")


def dump_config(opts):
    """
    Dump the configuration file
    """
    print("*** bsi-cli configuration")
    for key in sorted(opts.keys()):
        if key == 'func':
            continue
        print("{:>16} : {}".format(key, opts[key]))
    print("***")
    return 0


def main():
    global opts

    # parse the command line args
    opts = cliargs.parse(
        get_results, get_results_frames, get_results_asr, get_results_features, get_results_diarization, send_audio, dump_config
    )

    opts = DotMap(opts, _dynamic=False)

    if opts.apiid is None:
        die("no BEST_API_ID/apiid was specified (env or config file)")

    if opts.apitoken is None:
        die("no BEST_API_TOKEN/apitoken was specified (env or config file)")

    # invoke the subcommand
    return opts.func(opts)


if __name__ == '__main__':
    main()
