from time import sleep, time
from sys import stdout

__author__ = "Niklas Bohn, Andre Hollstein"


# noinspection PyDefaultArgument
def tqdm_joblist(jobs, update_intervall=1.0, max_update_intervall=10, n_status_prints=10, modify_jobs=True,
                 sleep_time=1.0, apply_on_done=None, status_prints=True, overprint=True, extra_args={}):
    """
    Monitor how a list of jobs submitted to a Pool becomes smaller as jobs become ready.

    :param overprint: TODO
    :param status_prints: True / False
    :param jobs: list og multiprocessing jobs
    :param apply_on_done: callable object, is called as ``apply_on_done(*job.get(),**extra_args)``
    :param extra_args: should be dictionary of extra args which is passed to apply_on_done
    :param modify_jobs: if True, then jobs is changed in place and is empty on return if false, the list remains
           unchanged -> this increases memory consumption (!)
    :param n_status_prints: number of wanted prints, wont be reached exactly if runtime ob jobs varies
    :param update_intervall: initial update time
    :param sleep_time: if fiven, additional sleep time in seconds
    :return: if apply_on_done given, then a list of results from apply_on_done is returned, order is nor preserved
    :raises: Nothing19
    """
    t0 = time()
    t_last_status_print = time()
    n_jobs = len(jobs)
    if apply_on_done is not None:
        job_results = []

    while jobs:
        # check which jobs are done, this is then used to split up the jobs
        readies = [job.ready() for job in jobs]  # must be consistent for done and not done jobs!
        jobs_done = [job for ready, job in zip(readies, jobs) if ready is True]
        if apply_on_done is not None:
            for job in jobs_done:
                inp = job.get()
                try:  # if inp is not a seqence, e.g. a scalar, then can't pass as *
                    job_results.append(apply_on_done(*inp, **extra_args))
                except TypeError:
                    job_results.append(apply_on_done(inp, **extra_args))
        else:
            for job in jobs:
                if job.ready():
                    job.get()
        del jobs_done  # delete rererences to jobs to let gc free memory
        # modify jobs in place to let the gc free the memory from the jobs which are done
        if modify_jobs:
            jobs[:] = [job for ready, job in zip(readies, jobs) if ready is False]
        else:
            jobs = [job for ready, job in zip(readies, jobs) if ready is False]
        # print eta, ... if wanted
        if status_prints:
            if ((n_jobs - len(jobs)) != 0) and (time() - t_last_status_print) > update_intervall:
                eta = (time() - t0) / (n_jobs - len(jobs)) * len(jobs)
                tot = (time() - t0) / (n_jobs - len(jobs)) * n_jobs
                update_intervall = tot / n_status_prints
                if update_intervall > max_update_intervall:
                    update_intervall = max_update_intervall

                t_last_status_print = time()
                msg = "Open Jobs: %i , eta: %.2fs~%.2fm~%.2fh, tot: %.2fs~%.2fm~%.2fh" % (
                    len(jobs), eta, eta / 60., eta / 3600.0, tot, tot / 60., tot / 3600.)
                if overprint:
                    stdout.write("\r%s" % msg)
                    stdout.flush()
                else:
                    print(msg)

            if (n_jobs - len(jobs)) == 0:
                msg = "Open Jobs: %i, time:%i" % (len(jobs), time())
                if overprint:
                    stdout.write("\r%s" % msg)
                    stdout.flush()
                    pass
                else:
                    print(msg)

        # if set, we sleep some time
        if sleep_time is not None:
            sleep(sleep_time)
    # return only if apply_on_done where given
    if apply_on_done is not None:
        return job_results


if __name__ == "__main__":
    print("Test")
    from multiprocessing import Pool

    def test(tt):
        sleep(tt)
        return tt

    def process(tt, jj):
        return tt * jj

    print("Simple")
    pp = Pool()  # max number of processes
    tqdm_joblist([pp.apply_async(func=test, args=(tt,)) for tt in 1000 * [0.001]], n_status_prints=10)
    pp.close()
    pp.join()  # wait for all runs to finish

    print("Call on done")
    pp = Pool()  # max number of processes
    print(tqdm_joblist([pp.apply_async(func=test, args=(tt,)) for tt in 20 * [0.5]],
                       n_status_prints=10,
                       apply_on_done=process,  # extra_args={"jj":10.3})
                       ))
    pp.close()
    pp.join()  # wait for all runs to finish
