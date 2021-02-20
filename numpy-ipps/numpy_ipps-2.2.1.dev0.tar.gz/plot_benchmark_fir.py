import json
import os

import numpy
import pylab


base_path = os.path.join(
    "log",
    "Linux-CPython-{}-64bit".format(os.environ["PYTHONVERSION"]),
)
for counter in ["0001", "0002"]:
    results = dict()
    try:
        with open(
            os.path.join(
                base_path,
                "{}_benchmark_py{}_{}.json".format(
                    counter,
                    os.environ["PYTHONVERSION"].replace(".", ""),
                    os.environ["PYTHONUPDATE"],
                ),
            )
        ) as json_file:
            for stats in json.load(json_file)["benchmarks"]:
                try:
                    fun = stats["name"].split("[", 1)[0]
                    if fun not in (
                        "test_ipps_fir_direct",
                        "test_ipps_iir_direct",
                        "test_ipps_iir_direct_biquad",
                        "test_ipps_median",
                        "test_ipps_iir_direct_I",
                        "test_ipps_iir_direct_biquad_I",
                        "test_ipps_median_I",
                        "test_ipps_fir_directFFT",
                        "test_ipps_fir_direct_cont",
                        "test_ipps_fir_directFFT_cont",
                        "test_ipps_median_cont",
                        "test_ipps_median_cont_I",
                        "test_ipps_fir_mr_direct",
                        "test_ipps_fir_mr_direct_cont",
                    ):
                        continue
                    ptype, pkernel, porder = stats["param"].split("-")
                except BaseException:
                    continue
                if fun not in results:
                    results[fun] = dict()
                if ptype not in results[fun]:
                    results[fun][ptype] = dict()
                if pkernel not in results[fun][ptype]:
                    results[fun][ptype][pkernel] = dict()
                if porder not in results[fun][ptype][pkernel]:
                    results[fun][ptype][pkernel][porder] = stats["stats"][
                        "ops"
                    ]
    except BaseException:
        continue

    figs_axes = dict()
    for fun in results.keys():
        for ptype in results[fun].keys():
            for n in results[fun][ptype].keys():
                fig_name = "{}_{}".format(ptype, n)
                if fig_name not in figs_axes:
                    fig = pylab.figure(figsize=(8.25, 8.25))
                    ax = fig.add_subplot(111)
                    figs_axes[fig_name] = (fig, ax)

                data = numpy.asarray(
                    [
                        [int(k), results[fun][ptype][n][k]]
                        for k in results[fun][ptype][n].keys()
                    ]
                )
                ind = numpy.argsort(data[:, 0])
                data = data[ind, :]

                figs_axes[fig_name][1].plot(
                    2 ** data[:, 0],
                    data[:, 1] * 2 ** data[:, 0],
                    "o-.",
                    label=fun,
                )

    for fig_name, (fig, ax) in figs_axes.items():
        ax.set_xscale("log")
        ax.set_yscale("log")

        ax.set_xlabel("Buffer size")
        ax.set_ylabel("FLOP/s")

        ax.legend()

        fig.tight_layout()
        fig.savefig(
            os.path.join(base_path, "{}-fir-{}.svg".format(counter, fig_name))
        )
