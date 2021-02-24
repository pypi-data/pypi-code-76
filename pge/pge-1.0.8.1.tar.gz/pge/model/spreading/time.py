import time
import numpy as np


class Spreading:
    @staticmethod
    def get_modeling_spreading_time_full_min(
        timer, model, num_iter, mx=None, prnt=False
    ):
        times = model.iteration_bunch(num_iter, mx=mx, prnt=prnt)
        df_times = [timer.get_times(int(mx_)) for mx_ in np.max(times, axis=1)]

        for i in np.arange(times.shape[0]):
            for j in np.arange(times.shape[1]):
                times[i, j] = np.sum(df_times[i][: int(times[i, j])])
        return {
            model.ids[i]: np.min(times[:, i]) for i in np.arange(model.graph.size())
        }

    @staticmethod
    def get_modeling_spreading_tick_full_min(model, num_iter, mx=None, prnt=False):
        times = model.iteration_bunch(num_iter, mx=mx, prnt=prnt)
        return {
            model.ids[i]: np.min(times[:, i]) for i in np.arange(model.graph.size())
        }

    @staticmethod
    def get_modeling_spreading_until_tick(model, num_iter, tick, prnt=False):
        return model.iteration_bunch_comm(num_iter, tick, prnt=prnt)

    @staticmethod
    def get_modeling_spreading_time_complex(timer, model, num_iter, comm, prnt=False):
        times = []
        comm_times = []

        for _ in np.arange(num_iter):
            k, n = model.iteration_bunch_complex(comm)
            df_times = timer.get_times(n)
            times.append(np.sum(df_times))
            comm_times.append(np.sum(df_times[:k]))
            if prnt:
                print("iteration", _)
        return comm_times, times

    @staticmethod
    def get_modeling_spreading_time_min_timer(model, num_iter):
        mx = None

        res = []
        for _ in np.arange(num_iter):
            toc = time.perf_counter()
            times = model.iteration_bunch(1, mx=mx, prnt=False)
            mx = np.max(times)
            res.append(time.perf_counter() - toc)
        return res

    @staticmethod
    def get_modeling_spreading_time_min_best_view(timer, model, size=None):
        nses = model.iteration_timer(size)
        times = timer.get_times(len(nses))

        ts = [np.sum(times[: i + 1]) for i in np.arange(len(nses))]
        speed = np.divide(ts, nses)
        return ts, speed, nses
