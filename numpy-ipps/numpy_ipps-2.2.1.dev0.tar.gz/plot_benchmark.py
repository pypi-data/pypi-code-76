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
                    params = stats["param"].split("-")
                    group, pkg, fun = (
                        stats["fullname"]
                        .replace(".py::test", "")
                        .split("[", 1)[0]
                        .split("_")[1:]
                    )
                    if len(params) == 2:
                        ptype, porder = params
                    elif len(params) == 3:
                        fun, ptype, porder = params
                except BaseException:
                    continue
                if pkg not in results:
                    results[pkg] = dict()
                if group not in results[pkg]:
                    results[pkg][group] = dict()
                if fun not in results[pkg][group]:
                    results[pkg][group][fun] = dict()
                if ptype not in results[pkg][group][fun]:
                    results[pkg][group][fun][ptype] = dict()
                if porder not in results[pkg][group][fun][ptype]:
                    results[pkg][group][fun][ptype][porder] = stats["stats"][
                        "ops"
                    ]
    except BaseException:
        continue

    figs_axes = dict()
    force_numpy = (dict(), dict())
    if "numpy" in results:
        for group in results["numpy"].keys():
            for fun in results["numpy"][group].keys():
                for ptype in results["ipps"][group][fun].keys():
                    if ptype not in results["numpy"][group][fun]:
                        continue
                    fig_name = "{}_{}".format(group, ptype)
                    if fig_name not in figs_axes:
                        fig = pylab.figure(figsize=(8.25, 8.25))
                        ax = fig.add_subplot(111)
                        figs_axes[fig_name] = (fig, ax)

                    data_ipps = numpy.asarray(
                        [
                            [int(k), results["ipps"][group][fun][ptype][k]]
                            for k in results["ipps"][group][fun][ptype].keys()
                        ]
                    )
                    ind = numpy.argsort(data_ipps[:, 0])
                    data_ipps = data_ipps[ind, :]
                    data_numpy = numpy.asarray(
                        [
                            [int(k), results["numpy"][group][fun][ptype][k]]
                            for k in results["ipps"][group][fun][ptype].keys()
                        ]
                    )
                    ind = numpy.argsort(data_numpy[:, 0])
                    data_numpy = data_numpy[ind, :]

                    L1_eff, L2_eff = 100 * data_ipps[:, 1] / data_numpy[:, 1]
                    if L2_eff > 120 and L1_eff > 120:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C0",
                        )
                    elif L1_eff > 80 and L2_eff > 80:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C1",
                        )
                    elif L1_eff > 80:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            100 ** 2 / L2_eff,
                            c="C3",
                        )
                        if fun not in force_numpy[0]:
                            force_numpy[0][fun] = []
                        force_numpy[0][fun].append((ptype, L1_eff, L2_eff))
                    else:
                        figs_axes[fig_name][1].scatter(
                            100 ** 2 / L1_eff,
                            100 ** 2 / L2_eff,
                            c="C7",
                        )
                        if fun not in force_numpy[1]:
                            force_numpy[1][fun] = []
                        force_numpy[1][fun].append((ptype, L1_eff, L2_eff))
                    figs_axes[fig_name][1].annotate(
                        fun,
                        (
                            L1_eff if L1_eff > 80 else 100 ** 2 / L1_eff,
                            L2_eff if L2_eff > 80 else 100 ** 2 / L2_eff,
                        ),
                    )

    with open(
        os.path.join(
            base_path,
            "{}_force_numpy_py{}_{}.json".format(
                counter,
                os.environ["PYTHONVERSION"].replace(".", ""),
                os.environ["PYTHONUPDATE"],
            ),
        ),
        "w",
    ) as force_numpy_file:
        force_numpy_file.write(json.dumps(force_numpy))

    for fig_name, (fig, ax) in figs_axes.items():
        ax.set_xscale("log")
        ax.set_yscale("log")

        L1_lim = ax.get_xlim()
        L2_lim = ax.get_ylim()

        ax.plot([100, L1_lim[1]], [80, 80], "k:")
        ax.plot([100, L1_lim[1]], [100, 100], "k--")
        ax.plot([100, L1_lim[1]], [120, 120], "k:")
        ax.plot([80, 80], [100, L2_lim[1]], "k:")
        ax.plot([100, 100], [100, L2_lim[1]], "k--")
        ax.plot([120, 120], [100, L2_lim[1]], "k:")

        ax.set_xlabel("IPP vs Numpy Ratio -- L1 Cache (%)")
        ax.set_ylabel("IPP vs Numpy Ratio -- L2 Cache (%)")

        fig.tight_layout()
        fig.savefig(
            os.path.join(base_path, "{}-{}.svg".format(counter, fig_name))
        )

    figs_axes = dict()
    disable_inplace = (dict(), dict())
    if "ipps" in results:
        for group in results["ipps"].keys():
            for fun in results["ipps"][group].keys():
                if fun[-2:] != "_I":
                    continue
                if fun[:-2] in results["ipps"][group]:
                    fun_outplace = fun[:-2]
                elif fun[1:-2] in results["ipps"][group]:
                    fun_outplace = fun[1:-2]
                else:
                    continue
                for ptype in results["ipps"][group][fun].keys():
                    if ptype not in results["ipps"][group][fun_outplace]:
                        continue
                    fig_name = "{}_{}_I".format(group, ptype)
                    if fig_name not in figs_axes:
                        fig = pylab.figure(figsize=(8.25, 8.25))
                        ax = fig.add_subplot(111)
                        figs_axes[fig_name] = (fig, ax)

                    data_inplace = numpy.asarray(
                        [
                            [int(k), results["ipps"][group][fun][ptype][k]]
                            for k in results["ipps"][group][fun][ptype].keys()
                        ]
                    )
                    ind = numpy.argsort(data_inplace[:, 0])
                    data_inplace = data_inplace[ind, :]
                    if fun[0] == "_":
                        data_outplace = numpy.asarray(
                            [
                                [
                                    int(k),
                                    results["ipps"][group][fun_outplace][
                                        ptype
                                    ][k],
                                ]
                                for k in results["ipps"][group][fun_outplace][
                                    ptype
                                ].keys()
                            ]
                        )
                    else:
                        data_outplace = numpy.asarray(
                            [
                                [
                                    int(k),
                                    results["ipps"][group][fun_outplace][
                                        ptype
                                    ][k],
                                ]
                                for k in results["ipps"][group][fun_outplace][
                                    ptype
                                ].keys()
                            ]
                        )
                    ind = numpy.argsort(data_outplace[:, 0])
                    data_outplace = data_outplace[ind, :]

                    L1_eff, L2_eff = (
                        100 * data_inplace[:, 1] / data_outplace[:, 1]
                    )
                    if L2_eff > 95 and L1_eff > 95:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C0",
                        )
                    elif L1_eff > 85 and L2_eff > 85:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C1",
                        )
                        if fun not in disable_inplace[0]:
                            disable_inplace[0][fun] = []
                        disable_inplace[0][fun].append((ptype, L1_eff, L2_eff))
                    else:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C3",
                        )
                        if fun not in disable_inplace[1]:
                            disable_inplace[1][fun] = []
                        disable_inplace[1][fun].append((ptype, L1_eff, L2_eff))
                    figs_axes[fig_name][1].annotate(fun, (L1_eff, L2_eff))

    with open(
        os.path.join(
            base_path,
            "{}_disable_inplace_py{}_{}.json".format(
                counter,
                os.environ["PYTHONVERSION"].replace(".", ""),
                os.environ["PYTHONUPDATE"],
            ),
        ),
        "w",
    ) as disable_inplace_file:
        disable_inplace_file.write(
            json.dumps(
                [
                    numpy.unique(disable_inplace[0]).tolist(),
                    numpy.unique(disable_inplace[1]).tolist(),
                ]
            )
        )

    for fig_name, (fig, ax) in figs_axes.items():
        ax.set_xscale("log")
        ax.set_yscale("log")

        L1_lim = ax.get_xlim()
        L2_lim = ax.get_ylim()

        ax.plot([100, L1_lim[1]], [80, 80], "k:")
        ax.plot([100, L1_lim[1]], [100, 100], "k--")
        ax.plot([100, L1_lim[1]], [120, 120], "k:")
        ax.plot([80, 80], [100, L2_lim[1]], "k:")
        ax.plot([100, 100], [100, L2_lim[1]], "k--")
        ax.plot([120, 120], [100, L2_lim[1]], "k:")

        ax.set_xlabel("Inplace vs Outplace Ratio -- L1 Cache (%)")
        ax.set_ylabel("Inplace vs Outplace Ratio -- L2 Cache (%)")

        fig.tight_layout()
        fig.savefig(
            os.path.join(base_path, "{}-{}.svg".format(counter, fig_name))
        )
