#
# service: OliverAPI: implement rest/swagger Oliver functionality
#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
#
#
import logging
import os
import json
import csv
import time
import requests
import aiohttp
import aiofiles
from copy import deepcopy
from ratelimit import limits, sleep_and_retry
from behavioral_signals_swagger_client import DefaultApi
from behavioral_signals_swagger_client.rest import ApiException

from .frames_csv import frames_to_csv
from .utils import max_timeout
from .settings import (MAX_REQUESTS_PER_SEC_PER_ENDPOINT, REQUESTS_LIMIT_PERIOD_SECS)


class RateLimitedApi(DefaultApi):

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_SEC_PER_ENDPOINT, period=REQUESTS_LIMIT_PERIOD_SECS)
    def rate_limited_get_process_info(self, cid, pid, **kwargs):

        def rate_limited_retry_get(response):
            try:
                results = response.get()
            except ApiException as e:
                if e.status == 429:
                    logging.warning("In get process info rate limiter kicked off, retrying in {}".format(REQUESTS_LIMIT_PERIOD_SECS))
                    time.sleep(REQUESTS_LIMIT_PERIOD_SECS)
                    response = self.rate_limited_get_process_info(cid, pid, **kwargs)
                    results = rate_limited_retry_get(response)
                else:
                    raise e

            return results

        response = self.get_process_info(cid, pid, **kwargs)
        response.rate_limited_retry_get = rate_limited_retry_get
        return response

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_SEC_PER_ENDPOINT, period=REQUESTS_LIMIT_PERIOD_SECS)
    def rate_limited_get_process_results(self, cid, pid, **kwargs):

        def rate_limited_retry_get(response):
            try:
                results = response.get()
            except ApiException as e:
                if e.status == 429:
                    logging.warning("In get results rate limiter kicked off, retrying in {}".format(REQUESTS_LIMIT_PERIOD_SECS))
                    time.sleep(REQUESTS_LIMIT_PERIOD_SECS)
                    response = self.rate_limited_get_process_results(cid, pid, **kwargs)
                    results = rate_limited_retry_get(response)
                else:
                    raise e

            return results

        response = self.get_process_results(cid, pid, **kwargs)
        response.rate_limited_retry_get = rate_limited_retry_get
        return response

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_SEC_PER_ENDPOINT, period=REQUESTS_LIMIT_PERIOD_SECS)
    def rate_limited_get_process_results_frames(self, cid, pid, **kwargs):

        def rate_limited_retry_get(response):
            try:
                results = response.get()
            except ApiException as e:
                if e.status == 429:
                    logging.warning("In get result farmes rate limiter kicked off, retrying in {}".format(REQUESTS_LIMIT_PERIOD_SECS))
                    time.sleep(REQUESTS_LIMIT_PERIOD_SECS)
                    response = self.rate_limited_get_process_results_frames(cid, pid, **kwargs)
                    results = rate_limited_retry_get(response)
                else:
                    raise e

            return results

        response = self.get_process_results_frames(cid, pid, **kwargs)
        response.rate_limited_retry_get = rate_limited_retry_get
        return response

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_SEC_PER_ENDPOINT, period=REQUESTS_LIMIT_PERIOD_SECS)
    def rate_limited_get_process_results_asr(self, cid, pid, **kwargs):

        def rate_limited_retry_get(response):
            try:
                results = response.get()
            except ApiException as e:
                if e.status == 429:
                    logging.warning("In get results asr rate limiter kicked off, retrying in {}".format(REQUESTS_LIMIT_PERIOD_SECS))
                    time.sleep(REQUESTS_LIMIT_PERIOD_SECS)
                    response = self.rate_limited_get_process_results_asr(cid, pid, **kwargs)
                    results = rate_limited_retry_get(response)
                else:
                    raise e

            return results

        response = self.get_process_results_asr(cid, pid, **kwargs)
        response.rate_limited_retry_get = rate_limited_retry_get
        return response

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_SEC_PER_ENDPOINT, period=REQUESTS_LIMIT_PERIOD_SECS)
    def rate_limited_get_process_results_diarization(self, cid, pid, **kwargs):

        def rate_limited_retry_get(response):
            try:
                results = response.get()
            except ApiException as e:
                if e.status == 429:
                    logging.warning("In get results diarization rate limiter kicked off, retrying in {}".format(REQUESTS_LIMIT_PERIOD_SECS))
                    time.sleep(REQUESTS_LIMIT_PERIOD_SECS)
                    response = self.rate_limited_get_process_results_diarization(cid, pid, **kwargs)
                    results = rate_limited_retry_get(response)
                else:
                    raise e

            return results


        response = self.get_process_results_diarization(cid, pid, **kwargs)
        response.rate_limited_retry_get = rate_limited_retry_get
        return response

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_SEC_PER_ENDPOINT, period=REQUESTS_LIMIT_PERIOD_SECS)
    def rate_limited_get_process_results_features(self, cid, pid, **kwargs):

        def rate_limited_retry_get(response):
            try:
                results = response.get()
            except ApiException as e:
                if e.status == 429:
                    logging.warning("In get results features rate limiter kicked off, retrying in {}".format(REQUESTS_LIMIT_PERIOD_SECS))
                    time.sleep(REQUESTS_LIMIT_PERIOD_SECS)
                    response = self.rate_limited_get_process_results_features(cid, pid, **kwargs)
                    results = rate_limited_retry_get(response)
                else:
                    raise e

            return results

        response = self.get_process_results_features(cid, pid, **kwargs)
        response.rate_limited_retry_get = rate_limited_retry_get
        return response


class OliverAPI():

    def __init__(self, opts, polling_time=5, indent=1):
        self.indent = indent
        self.opts = opts
        self.api = RateLimitedApi()
        self.api.api_client.configuration.host = opts.apiurl
        self.api.api_client.configuration.api_key['X-Auth-Token'] = opts.apitoken
        self.polling_time = polling_time

        self.transients_count = 0

    def __del__(self):
        """
        Manually close thread pool of swagger generated client.
        This handles a known bug on python 3.5 Garbage Collection
        """
        try:
            self.api.api_client.pool.close()
            self.api.api_client.pool.join()
        except Exception:
            pass

    def get_client_details(self):
        url = "{}/client/{}".format(self.opts.apiurl, self.opts.apiid)

        headers = {'X-Auth-Token': self.opts.apitoken, 'Accept': "application/json"}

        r = requests.get(url, headers=headers)

        logging.debug(r.url)
        logging.debug(r.text)

    def authorized(self):
        url = "{}/client/{}".format(self.opts.apiurl, self.opts.apiid)

        headers = {'X-Auth-Token': self.opts.apitoken, 'Accept': "application/json"}

        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except Exception:
            return False

        return True

    def send_audio(self, files, data):
        """
        Submit audio file to API
        """
        process_audio_url = "{}/client/{}/process/audio".format(self.opts.apiurl, self.opts.apiid)

        headers = {'X-Auth-Token': self.opts.apitoken, 'Accept': "application/json"}

        response = requests.post(
            process_audio_url, params=data, files=files, headers=headers
        )

        if response.status_code == 401:
            raise ValueError("Permission denied. Authentication required to use the resource")

        return response

    def GetInfo(self, pid, poll=False):
        """
        Obtain process info and poll if necessary
        """
        elapsed_time = 0

        wait, resp = self.getInfo(pid)

        if not poll:
            return resp

        while wait:
            time.sleep(self.polling_time)
            elapsed_time += self.polling_time
            wait, resp = self.getInfo(pid)

        if elapsed_time > 0:
            logging.info("{} : polled process for {} seconds". format(pid, elapsed_time))

        return resp

    def GetResults(self, pid, output_dir=None, dest=None):
        """
        Obtain process results and dump them to a file
        """
        results = {}

        try:
            results = self.api.rate_limited_get_process_results(self.opts.apiid, pid)
            results = results.to_dict()
        except ValueError as e:
            if str(e) == "Invalid value for `basic`, must not be `None`":
                logging.warning("{}: No process results output".format(pid))
            else:
                logging.warning("{}: Process failed: {}".format(pid, e))
                results = None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: Process Results failure: {}/{}".format(pid, msg, e.status))
                results = None
            else:
                raise e
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, pid=pid)

        return results

    def GetFrameResults(self, pid, output_dir=None, dest=None):
        """
        Obtain frame results and dump them to a file
        """
        results = {}

        try:
            results = self.api.rate_limited_get_process_results_frames(self.opts.apiid, pid)
            results = results.to_dict()
        except ValueError as e:
            if str(e) == "Invalid value for `frames`, must not be `None`":
                logging.warning("{}: No frames results output".format(pid))
            else:
                logging.warning("{}: Process failed: {}".format(pid, e))
                results = None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: Frame Results failure: {}/{}".format(pid, msg, e.status))
                results = None
            else:
                raise e
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, "_frames", pid=pid)

        return results

    def GetASRResults(self, pid, output_dir=None, dest=None):
        """
        Obtain ASR results from Oliver API
        """
        results = {}

        try:
            results = self.api.rate_limited_get_process_results_asr(self.opts.apiid, pid)
            results = results.to_dict()

            if results.get("predictions") is None:
                results.pop("predictions", None)

        except ValueError as e:
            # -- in case there is no ASR record for it
            if str(e) == "Invalid value for `words`, must not be `None`":
                logging.warning("{}: No ASR output".format(pid))
            else:
                logging.warning("{}: ASR failed: {}".format(pid, e))
                results = None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: ASR failure: {}/{}".format(pid, msg, e.status))
                results = None
            else:
                raise e
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, "_words", pid=pid)

        return results

    def GetFeaturesResults(self, pid, output_dir=None, dest=None):
        """
        Obtain feature results and dump them to a file
        """
        results = {}

        try:
            results = self.api.rate_limited_get_process_results_features(self.opts.apiid, pid)
            results = results.to_dict()
        except ValueError as e:
            if str(e) == "Invalid value for `features`, must not be `None`":
                logging.warning("{}: No features results output".format(pid))
            else:
                logging.warning("{}: Process failed: {}".format(pid, e))
                results = None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: Feature Results failure: {}/{}".format(pid, msg, e.status))
                results = None
            else:
                raise e
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, "_features", pid=pid)

        return results

    def GetDiarizationResults(self, pid, output_dir=None, dest=None):
        """
        Obtain feature results and dump them to a file
        """
        results = {}

        try:
            results = self.api.rate_limited_get_process_results_diarization(self.opts.apiid, pid)
            results = results.to_dict()
        except ValueError as e:
            if str(e) == "Invalid value for `diarization`, must not be `None`":
                logging.warning("{}: No diarization results output".format(pid))
            else:
                logging.warning("{}: Process failed: {}".format(pid, e))
                results = None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: Diarization Results failure: {}/{}".format(pid, msg, e.status))
                results = None
            else:
                raise e
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, "_diarization", pid=pid)

        return results

    async def send_audio_async(self, session, pidsfile, filepath, filename, **params):
        audio_url = "{}/client/{}/process/audio".format(self.opts.apiurl, self.opts.apiid)

        data = aiohttp.FormData()

        try:
            async with aiofiles.open(filepath, mode='rb') as f:
                filedata = await f.read()
        except FileNotFoundError:
            logging.warning("Not found {}".format(filepath))
            return
        except Exception as e:
            logging.warning("Error while reading data from {}, error: {}".format(filepath, e))
            return

        data.add_field('file', filedata, filename=filename)

        try:
            timeout = max_timeout(len(filedata)) * self.opts.uploads

            async with session.post(audio_url, data=data, params=params, timeout=timeout) as response:
                r = await response.json()

                if response.status == 200:
                    await pidsfile.write("{}\n".format((r['pid'])))
                else:
                    logging.warning("Service responded with status {}, message: {}, when uploading audio file: {}".format(
                        response.status, r['message'], filename)
                    )

        except Exception as e:
            logging.warning("Error while uploading {}, error: {}".format(filepath, e))

    def getInfoAsync(self, pids, poll=False):
        pids_statuses = {}
        ready = {}
        transient = set()
        failed = set()

        polling_pids = deepcopy(pids)

        while True:
            for pid in polling_pids:
                resp = self.api.rate_limited_get_process_info(self.opts.apiid, pid, async_req=True)
                pids_statuses[pid] = resp

            for pid, ps in pids_statuses.items():
                try:
                    result = ps.rate_limited_retry_get(ps)
                except Exception as e:
                    if e.status == 404:
                        logging.warning("Not found process with id {}".format(pid))
                        failed.add(pid)
                        continue
                    else:
                        raise e

                if result.status == 2:
                    ready[result.pid] = result.source
                    transient.discard(pid)
                    polling_pids.remove(pid)
                elif result.status == -1:
                    transient.add(pid)
                elif result.status == -2:
                    failed.add(pid)
                    transient.discard(pid)
                    polling_pids.remove(pid)

            if ready:
                self.transients_count = 0
                break

            if failed:
                self.transients_count = 0
                break

            if self.transients_count >= 3:
                time.sleep(self.polling_time)
                break

            if not poll or len(transient) == len(pids):
                self.transients_count += 1
                break

            pids_statuses.clear()
            time.sleep(self.polling_time)

        return ready, list(transient), list(failed)

    def GetResultsAsync(self, processes, output_dir=None):
        results = {}
        responses = {}
        noresult_pids = []

        for pid in processes:
            response = self.api.rate_limited_get_process_results(self.opts.apiid, pid, async_req=True)
            responses[pid] = response

        for pid, response in responses.items():
            try:
                results = response.rate_limited_retry_get(response)
                results = results.to_dict()
            except ValueError:
                noresult_pids.append(pid)
                results = None
            except Exception as e:
                if e.status == 405 or e.status == 503:
                    msg = self.getResponse(e.body, 'message')
                    logging.warning("{}: Process results failure: {}/{}".format(pid, msg, e.status))
                    results = None
                else:
                    raise e

                noresult_pids.append(pid)
            finally:
                if results is not None:
                    self.saveOutput2File(results, output_dir, processes[pid], pid=pid)

        return noresult_pids

    def GetFrameResultsAsync(self, processes, output_dir=None):
        responses = {}
        results = {}
        noresult_pids = []

        for pid in processes:
            response = self.api.rate_limited_get_process_results_frames(self.opts.apiid, pid, async_req=True)
            responses[pid] = response

        for pid, response in responses.items():
            try:
                results = response.rate_limited_retry_get(response)
                results = results.to_dict()
            except ValueError:
                noresult_pids.append(pid)
                results = None
            except Exception as e:
                if e.status == 405 or e.status == 503:
                    msg = self.getResponse(e.body, 'message')
                    logging.warning("{}: Frame Results failure: {}/{}".format(pid, msg, e.status))
                    noresult_pids.append(pid)
                    results = None
                else:
                    raise e
            finally:
                if results is not None:
                    self.saveOutput2File(results, output_dir, processes[pid], "_frames", pid=pid)

        return noresult_pids

    def GetASRResultsAsync(self, processes, output_dir=None):
        responses = {}
        results = {}
        noresult_pids = []

        for pid in processes:
            response = self.api.rate_limited_get_process_results_asr(self.opts.apiid, pid, async_req=True)
            responses[pid] = response

        for pid, response in responses.items():
            try:
                results = response.rate_limited_retry_get(response)
                results = results.to_dict()

                if results.get("predictions") is None:
                    results.pop("predictions", None)
            except ValueError:
                noresult_pids.append(pid)
                results = None
            except Exception as e:
                if e.status == 405 or e.status == 503:
                    msg = self.getResponse(e.body, 'message')
                    logging.warning("{}: ASR failure: {}/{}".format(pid, msg, e.status))
                    results = None
                else:
                    raise e
            finally:
                if results is not None:
                    self.saveOutput2File(results, output_dir, processes[pid], "_words", pid=pid)

        return noresult_pids

    def GetDiarizationResultsAsync(self, processes, output_dir=None):
        responses = {}
        results = {}
        noresult_pids = []

        for pid in processes:
            response = self.api.rate_limited_get_process_results_diarization(self.opts.apiid, pid, async_req=True)
            responses[pid] = response

        for pid, response in responses.items():
            try:
                results = response.rate_limited_retry_get(response)
                results = results.to_dict()

                if results.get("predictions") is None:
                    results.pop("predictions", None)
            except ValueError:
                noresult_pids.append(pid)
                results = None
            except Exception as e:
                if e.status == 405 or e.status == 503:
                    msg = self.getResponse(e.body, 'message')
                    logging.warning("{}: Diarization failure: {}/{}".format(pid, msg, e.status))
                    noresult_pids.append(pid)
                    results = None
                else:
                    raise e
            finally:
                if results is not None:
                    self.saveOutput2File(results, output_dir, processes[pid], "_diarization", pid=pid)

        return noresult_pids

    def GetFeaturesResultsAsync(self, processes, output_dir=None, dest=None):
        """
        Obtain feature results and dump them to a file
        """
        responses = {}
        results = {}
        noresult_pids = []

        for pid in processes:
            response = self.api.rate_limited_get_process_results_features(self.opts.apiid, pid, async_req=True)
            responses[pid] = response

        for pid, response in responses.items():
            try:
                results = response.rate_limited_retry_get(response)
                results = results.to_dict()
            except ValueError:
                noresult_pids.append(pid)
                results = None
            except Exception as e:
                if e.status == 405 or e.status == 503:
                    msg = self.getResponse(e.body, 'message')
                    logging.warning("{}: Feature Results failure: {}/{}".format(pid, msg, e.status))
                    noresult_pids.append(pid)
                    results = None
                else:
                    raise e
            finally:
                if results is not None:
                    self.saveOutput2File(results, output_dir, dest, "_features", pid=pid)

        return noresult_pids

    def getInfo(self, pid):
        """
        Obtain process info
        """
        try:
            resp = self.api.rate_limited_get_process_info(self.opts.apiid, pid)
        except Exception as e:
            if e.status == 404:
                return False, None
            else:
                raise e

        if resp.status == -1:
            logging.info("{}: transient error -- retrying".format(pid))
            return False, resp

        if resp.status in [0, 1]:
            return True, resp

        return False, resp

    def saveOutput2File(self, results, output_dir, dest, suffix="", pid=0):
        """
        Save results to `json` or `csv` file
        """
        if not output_dir:
            return
        if not dest:
            return

        fname = os.path.splitext(os.path.basename(dest))[0]

        if "csv" in self.opts and self.opts.csv:
            csv_file = os.path.join(output_dir, "{}_{}{}.csv".format(fname, pid, suffix))
            results = frames_to_csv(results)

            with open(csv_file, "w") as fp:
                csv_writer = csv.writer(fp, delimiter=",")
                for row in results:
                    csv_writer.writerow(row)

        else:
            json_file = os.path.join(output_dir, "{}_{}{}.json".format(fname, pid, suffix))
            with open(json_file, 'w') as jf:
                json.dump(results, jf, indent=self.indent)

    def getResponse(self, body, attr):
        """
        Returns response body jsonified or special identifier
        """
        try:
            r = json.loads(body)
            return r[attr]
        except Exception:
            return "?"
