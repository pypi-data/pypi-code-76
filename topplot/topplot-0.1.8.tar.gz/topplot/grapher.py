# Copyright (c) 2019-2020 Jonathan Sambrook and Codethink Ltd.
#
#    This file is part of Topplot.
#
#    Topplot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Topplot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Topplot.  If not, see <https://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------
# Grapher has one or more FigManagers.
# FigManager has one figure with one or more plots/subplots and implements
# per-figure functionality.
# Grapher constructs figures, plots the data, and performs supra-FigManager
# functions too.
# -----------------------------------------------------------------------------

# pylint: disable=too-many-lines # C0302: Too many lines in module (>1000)

import math
import re
import sys
from typing import Any, Dict, List, Tuple

import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from .figman import FigManager
from .linestyler import LineStyler

from .utils import die, warn

try:
    import mplcursors

    mplcursors_present = True
except ImportError:
    print(
        "The mplcursors Python module is not installed, so annotations are not"
        " available. Hint: pip3 install mplcursors"
    )
    mplcursors_present = False

# -----------------------------------------------------------------------------
# Select GUI toolkit

mpl.use("TKAgg")

# -----------------------------------------------------------------------------
# Add mplcursors annotation capability for the given axis' lines, if available.


def add_annotations(figman, ax):
    if "mplcursors" in sys.modules:
        c = mplcursors.Cursor(hover=False, multiple=True, artists=tuple(ax.get_lines()))

        # At the time of writing (mpl 3.1.0) mpl doesn't allow consuming of gui
        # events, so they're propogated to all hooks. Which means that
        # mplcursors annotations are triggered even when they are underneath
        # legends.
        # This on_add closure callback fixes that situation.
        def on_add(sel):
            # Convert from data co-ords to display co-ords
            x, y = ax.transData.transform(tuple(sel.target))

            # Cycle through axes' legends checking for hits
            fake_event = mpl.backend_bases.MouseEvent("dummy", figman.fig.canvas, x, y)

            for legend in figman.get_legends():
                result, _ = legend.contains(fake_event)

                # Remove sel on hit
                if result:
                    c.remove_selection(sel)

        c.connect("add", on_add)


# -----------------------------------------------------------------------------
# Customize MatPlotLib rcParams for topplot


def override_rcParams():
    mpl.rcParams["legend.facecolor"] = "white"  # Doesn't work
    mpl.rcParams["legend.fancybox"] = True
    mpl.rcParams["legend.shadow"] = True
    # Disable keystrokes for toggling log scales
    mpl.rcParams["keymap.xscale"] = []
    mpl.rcParams["keymap.yscale"] = []
    # Remove clashes with topplot's keymap
    mpl.rcParams["keymap.back"] = filter(
        lambda x: x != "c", mpl.rcParams["keymap.back"]
    )


# -----------------------------------------------------------------------------
# Dump MatPlotLib rcParams


def rcParams():
    # Override defaults
    override_rcParams()

    # Dump state
    for k, v in mpl.rcParams.items():
        print(f"mpl.rcParams['{k}'] = {v}")


# -----------------------------------------------------------------------------
# Turn on H:M:S date format for the given axis


def set_x_axis_time_formatting(ax):
    ax.xaxis.axis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))


# -----------------------------------------------------------------------------
# Class to encapsulate the graphing side of topplot


class Grapher:

    # -------------------------------------------------------------------------

    def __init__(
        self,
        graph_map,
        config,
        data,
        cores,
        mem_unit,
        mem_cached_or_available,
        progress_window,
    ):
        self.at_close = None
        self.config = config
        self.cores = cores
        self.data = data
        self.mem_unit = mem_unit
        self.graph_map = graph_map
        self.progress_window = progress_window
        width, height = progress_window.get_curr_screen_dimensions(scale=0.9)
        self.window_size = f"{width}x{height}"

        self.display_legends = True

        self.linestyler = LineStyler()

        self.fig_manager = {}

        self.mem_cached_or_available = mem_cached_or_available.replace("_", " ")
        self.mplcursors_present = mplcursors_present

        self.colours = {
            "combined": "red",
            "poi_cpu": "red",
            "poi_mem": "blue",
            "user": "green",
            "system": "red",
            "nice": "blue",
            "idle": (0.3, 0.3, 0.3),
            "wait": "black",
            "hw irq": "orange",
            "sw irq": "cyan",
            "steal": "gray",
            "exec": "chartreuse",
            "task running": "green",
            "task sleeping": "blue",
            "task stopped": "red",
            "task zombie": "black",
            "mem used": "blue",
            "mem free": "green",
            "mem buffers": "pink",
            self.mem_cached_or_available: "green",
            "swap free": "purple",
            "load average": "purple",
            "fig_face": (  # Equivalent to ProgressWindow's __init__().bg = "#F2F2E6".
                0.95,
                0.95,
                0.90,
            ),  # Keep in sync.
        }

        self.markers = {
            "user": "$u$",
            "system": "$s$",
            "nice": "$n$",
            "idle": "$i$",
            "wait": "$w$",
            "hw irq": "$hw$",
            "sw irq": "$sw$",
            "steal": "$st$",
            "exec": "$x$",
        }

        if cores > 1:
            for core in range(cores):
                tmp = {}
                for (k, v) in self.markers.items():
                    tmp[f"{core}{k}"] = f"{v}{core}"
                if tmp:
                    self.markers.update(tmp)

        self.cartesian_map = [[None, None], [None, None]]

    # -------------------------------------------------------------------------
    # Convert from four-by-one array index to two-by-two array index

    def ordinal_to_cartesian_map(self, n):
        x = int(n / 2)
        y = n % 2
        return self.cartesian_map[x][y]

    # -------------------------------------------------------------------------
    # Apply the relevant style to the lines on the given axis/axes

    def style_lines(self, *axes):
        for ax in axes:
            prefix = ""
            label = ax.get_yaxis().get_label().get_text()
            if label is not None:
                prefix = label
            for line in ax.get_lines():
                self.linestyler.style(prefix + line.get_label(), line)

    # -------------------------------------------------------------------------
    # Common title formatting

    def title(self, text):
        return f"topplot : {self.config.toplog_filename} : {text}"

    # -------------------------------------------------------------------------
    # Styles for any/all axes

    @staticmethod
    def common_axes(figman, ax):
        ax.set_facecolor("white")
        ax.margins(0)
        ax.set_xlabel("")
        set_x_axis_time_formatting(ax)
        add_annotations(figman, ax)

    # -------------------------------------------------------------------------
    # Styles for 'primary' axes

    def common_ax1(self, figman, ax):
        self.common_axes(figman, ax)
        ax.grid(linestyle=":", linewidth="0.5", color="black", alpha=0.5)

    # -------------------------------------------------------------------------
    # Styles for 'secondary' axes

    def common_ax2(self, figman, ax):
        self.common_axes(figman, ax)
        ax.grid(linestyle="--", linewidth="0.5", color="black", alpha=0.75)

    # -------------------------------------------------------------------------
    # Map legend lines to plotted lines
    # An mpl API workaround is required

    @staticmethod
    def pickable_legend_lines(figman, legend, ax1, ax2=None, len1=None):
        leglines = legend.get_lines()
        legtexts = legend.get_texts()

        # WARNING: going off mpl API here to get the legend's handles
        leghandles = legend.legendHandles

        # WARNING: going off mpl API here to access the artist of the legend's title box
        title = legend._legend_title_box._text  # pylint: disable=protected-access

        if len1 is None:
            len1 = len(ax1.get_lines())

        if len1 > 0:
            figman.map_legend_lines(
                ax1,
                title,
                leglines=leglines[:len1],
                legtexts=legtexts[:len1],
                leghandles=leghandles[:len1],
            )

        if ax2 is not None:
            figman.map_legend_lines(
                ax2,
                title,
                leglines=leglines[len1:],
                legtexts=legtexts[len1:],
                leghandles=leghandles[len1:],
            )

    # -------------------------------------------------------------------------
    # Produce a legend for a single axis

    def single_legend(self, figman, title, legtitle, ax_ylabel, ax, *, cap=None):
        # Set furniture text
        ax.set_title(title)
        ax.set_ylabel(ax_ylabel)

        # Get legend lines ready
        handles, labels = ax.get_legend_handles_labels()

        if cap is not None:
            handles = handles[0:cap]
            labels = labels[0:cap]

        # Generate new legend
        legend = ax.legend(handles, labels, loc="upper right", title=legtitle)
        legend.set_draggable(True)

        self.pickable_legend_lines(figman, legend, ax)

    # -------------------------------------------------------------------------
    # Produce an extra one-to-many (otm) legend to enable togging of a particular
    # measurement in a single plot displaying all CPU cores.

    @staticmethod
    def otm_legend(
        figman,
        legtitle,
        prefix_regex,
        ax,
        src_legend,
        *,
        loc="upper right",
        copy_markers=True,
    ):
        re_prefix = re.compile(prefix_regex)
        re_trailing_digits = re.compile(r"\d+$")

        categories = {}

        # Sort out toggleable elements
        for (legline, handle, text) in zip(
            src_legend.get_lines(), src_legend.legendHandles, src_legend.texts
        ):
            label = text.get_text()
            match = re_prefix.match(label)
            if match is not None:
                category = match.group(1)
                legelts = [figman.legtexts[legline], figman.legmarkers[legline]]
                if category not in categories:
                    marker = (
                        handle._legmarker.get_marker()  # pylint: disable=protected-access
                    )
                    marker = re_trailing_digits.sub("", marker, 1)
                    categories[category] = {
                        "lines": [handle],
                        "legelts": legelts,
                        "colour": handle.get_color(),
                        "lw": handle.get_linewidth(),
                        "marker": marker,
                    }
                else:
                    categories[category]["lines"].append(handle)
                    categories[category]["legelts"] += legelts

        # Create shiney new legend lines
        new_handles = []
        new_labels = []
        for category in categories:
            extra_args = {"lw": categories[category]["lw"]}
            if copy_markers:
                extra_args["marker"] = categories[category]["marker"]
            line = mpl.lines.Line2D(
                [],
                [],
                color=categories[category]["colour"],
                label=category,
                **extra_args,
            )
            new_handles.append(line)
            new_labels.append(category)

        # Generate new legend
        legend = plt.legend(new_handles, new_labels, loc=loc, title=legtitle)
        figman.register_legend(ax, legtitle, legend)
        legend.set_draggable(True)

        for (line, text) in zip(legend.get_lines(), legend.get_texts()):
            label = line.get_label()
            line.set_pickradius(10)
            text.set_picker(10)
            figman.legotm[line] = categories[label]["lines"]
            figman.legotm[text] = categories[label]["lines"]

        # Re-add src legend since it will have been detached by the
        # plt.legend([..]) call above
        ax.add_artist(src_legend)

        return legend

    # -------------------------------------------------------------------------
    # Combine legends from both axes in to single axis

    def combined_legend(
        self,
        figman,
        title,
        legtitle,
        ax1_ylabel,
        ax2_ylabel,
        ax1,
        ax2,
        *,
        cap1=None,
        cap2=None,
        location="upper right",
    ):
        # Set furniture text
        ax2.set_title(title)
        ax1.set_ylabel(ax1_ylabel)
        ax2.set_ylabel(ax2_ylabel)

        # Get legend lines ready
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()

        if cap1 is not None:
            handles1 = handles1[0:cap1]
            labels1 = labels1[0:cap1]

        if cap2 is not None:
            handles2 = handles2[0:cap2]
            labels2 = labels2[0:cap2]

        # Remove original legends from drawing tree
        ax1.get_legend().remove()
        ax2.get_legend().remove()

        # Generate new legend
        legend = ax2.legend(
            handles1 + handles2, labels1 + labels2, loc=location, title=legtitle
        )
        legend.set_draggable(True)
        ax2.get_legend().set_draggable(True)

        self.pickable_legend_lines(figman, legend, ax1, ax2, len1=len(handles1))

        return legend

    # -------------------------------------------------------------------------

    @staticmethod
    def generate_markeveries(
        row_count: int, col_count: int, total_markers: int
    ) -> List[Tuple[int, int]]:
        """Generate a list of (offset, markevery) tuples for a dataset of the given dimensions.

        Makes an attempt to avoid clustering markers on different lines.

        Args:
            row_count (int): How many rows in the dataset.
            col_count (int): How many columns in the dataset.
            total_markers (int): How many markers are required for each line.

        Returns:
            list: The generated (offset, markevery) tuples.
        """
        markeveries = []

        # Calculate offsets for markers so that they don't cluster
        clustering = True

        markevery = int(row_count / total_markers)

        # Loop if offsets are (still) clustered and another attempt makes sense
        while clustering and total_markers >= 1:
            offset_prev = None
            for col in range(col_count):
                offset = int(markevery / col_count) * col
                if offset_prev is not None and offset_prev != offset:
                    clustering = False
                offset_prev = offset
                markeveries.append((offset, markevery))
            total_markers -= 1

        return markeveries

    # -------------------------------------------------------------------------
    # Draw the load average and CPU graph
    #
    # Forcing a single cpu core isn't the same as there being no multicore data.
    # Forcing a single core displays the core's index in labels, and removes the
    # load average display since that's not relevant to a single core out of
    # multiple cores.

    def graph_cpus(
        self,
        figman,
        df,
        ax_in,
        title,
        *,
        x_bounds=None,
        force_single_core: bool = None,
        overview: bool = False,
    ):
        ax_loadavg = None

        if force_single_core is None:
            ax_loadavg = ax_in
            ax_cpu = ax_loadavg.twinx()
            legend_title = "cpu/load"
        else:
            ax_cpu = ax_in
            legend_title = "cpu"

        if force_single_core is None:
            df.plot(
                y="load average",
                color=self.colours["load average"],
                ax=ax_loadavg,
                lw=3,
            )

        measures = ["user", "system", "nice", "idle", "wait", "hw irq", "sw irq"]

        if self.config.with_cpu_steal:
            measures.append("steal")

        core_test = 0 if force_single_core is None else force_single_core
        colname_test = "cpu exec" if self.cores == 1 else f"cpu{core_test} exec"
        if colname_test in df.columns:
            measures = ["exec"] + measures

        if self.cores > 1 or force_single_core is not None:
            # never display line markers for overview, and only if ordered to otherwise
            display_cpu_markers = False if overview else self.config.display_cpu_markers

            if display_cpu_markers:
                # To put text markers on each line has two cost implications
                #  i) df.plot() doesn't handle lists of markers/markeveries, so
                #     you need a two level loop and (cores * len(measures)) calls
                #     to df.plot()
                # ii) the markers trigger mathstext font related calls.
                #     Informative result, but slow.

                markeveries = self.generate_markeveries(len(df), self.cores, 10)

                for core in (
                    range(0, self.cores)
                    if force_single_core is None
                    else [force_single_core]
                ):
                    for measure in measures:
                        extra_args : Dict[str, Any] = {}
                        if force_single_core is None:
                            # The dollar symbols trigger lots of calling of
                            # expensive mathtext font functions
                            extra_args["marker"] = f"${core}$"
                            extra_args["markevery"] = markeveries[core]
                            extra_args["markersize"] = 8

                        df.plot(
                            y=f"cpu{core} {measure}",
                            color=self.colours[measure],
                            ax=ax_cpu,
                            **extra_args,
                        )
            else:  # This is the fast-but-no-markers version
                labels = []
                colours = []

                for measure in measures:
                    for core in (
                        range(0, self.cores)
                        if force_single_core is None
                        else [force_single_core]
                    ):
                        labels.append(f"cpu{core} {measure}")
                        colours.append(self.colours[measure])

                df.plot(
                    y=labels,
                    color=colours,
                    ax=ax_cpu,
                )
        else:  # Single core (forced or natural)
            labels = []
            colours = []

            for measure in measures:
                labels.append(f"cpu {measure}")
                colours.append(self.colours[measure])

            df.plot(
                y=labels,
                color=colours,
                ax=ax_cpu,
            )

        # Legend(s)
        if force_single_core is None and self.cores > 1:
            combined_legend = self.combined_legend(
                figman,
                title,
                legend_title,
                "loadavg",
                "cpu (%)",
                ax_loadavg,
                ax_cpu,
                location="upper left",
            )  # , cap2=len(measures))

            self.otm_legend(
                figman,
                "cpu(grouped)/load",
                # strip any leading "cpu0 ", "cpu1 ", ..
                r"^(?:cpu\d+ )?(.+)",
                ax_cpu,
                combined_legend,
                copy_markers=False,
            )

            if overview:
                combined_legend.remove()

        else:
            self.single_legend(figman, title, legend_title, "cpu (%)", ax_cpu)

        # Axes fettling
        if force_single_core is None and ax_loadavg:
            ax_loadavg.tick_params("x", which="minor", bottom=False)
            self.common_ax1(figman, ax_loadavg)
            ax_loadavg.set_ybound(lower=0, upper=df["load average"].max() * 105.0 / 100)

        if x_bounds is not None:
            min_timestamp, max_timestamp = x_bounds
            ax_cpu.set_xbound(lower=min_timestamp, upper=max_timestamp)

        self.common_ax2(figman, ax_cpu)
        ax_cpu.set_ybound(lower=0, upper=100)

    # -------------------------------------------------------------------------
    # Draw the task summary graph

    def graph_tasks(
        self,
        figman,
        df_in,
        ax_sleeping,
        title,
        overview: bool = False,  # pylint: disable=unused-argument
    ):

        ax_others = ax_sleeping.twinx()

        df = df_in.rename(columns=lambda x: x[5:] if x[:5] == "task " else x)
        df.filter(items=["sleeping"]).plot(
            ax=ax_sleeping, color=self.colours["task sleeping"], x_compat=True
        )

        task_colours = []
        items = ["running", "stopped", "zombie"]
        for item in items:
            task_colours.append(self.colours["task " + item])
        df.filter(items=items).plot(ax=ax_others, color=task_colours, x_compat=True)

        self.combined_legend(
            figman,
            title,
            "tasks",
            "sleeping tasks",
            "running, stopped, and zombie tasks",
            ax_sleeping,
            ax_others,
        )
        self.common_ax1(figman, ax_sleeping)
        self.common_ax2(figman, ax_others)
        ax_others.set_ybound(lower=0)
        ax_sleeping.set_ybound(lower=0, upper=df["sleeping"].max() * 105.0 / 100)

    # -------------------------------------------------------------------------
    # Draw the memory summary graph

    def graph_mem(
        self,
        figman,
        df,
        ax1,
        title,
        overview: bool = False,  # pylint: disable=unused-argument
    ):
        ax1.set_title(title)

        mem_colours = []

        # Draw 'mem free' lowest in z-order, unless 'mem availble' is needed there
        lowest_mem = (
            "mem free"
            if self.mem_cached_or_available == "mem cached"
            else "mem available"
        )

        items = [lowest_mem, "mem used", "mem buffers"]
        for item in items:
            mem_colours.append(self.colours[item])
        df.filter(items=items).plot.area(ax=ax1, color=mem_colours)

        # Inform the user if it looks like top's scale was set too high
        if df.iloc[[0, -1]].sum(axis=1).sum() == 0.0:
            msg = (
                "The memory and swap values for the first and last cycles are all zero."
                " Was top's scale set too high?\nToggle through the available scales by"
                " pressing uppercase 'E' in top's Interactive mode's main page.\nThen"
                " save the config by press uppercase 'W'."
            )
            figman.display_msg(msg, 5)
            print(f"WARNING: {msg}")

        # 'mem used' includes 'mem cached' which is pants, since that memory is
        # available to use immediately, although if the VFS is asked for its old
        # contents and they're still valid, it will (immediately) be put back to use
        # as that data instead.  ('mem available' handles this better.)
        #
        # Indicate this state of affairs by colouring cached memory using the colours
        # for 'mem free' hatched with 'mem used'

        if self.mem_cached_or_available == "mem cached":
            # Overwrite the overlapping part of 'mem used' with 'mem cached'
            df.filter(items=["mem free", "mem cached"]).plot.area(
                ax=ax1, color=self.colours["mem free"]
            )
            chatch = ax1.collections[-1]

            # Knock out confusing repeat 'mem free' legend
            c = ax1.collections[-2]
            c.set_label("")
        else:
            # Overwrite the overlapping part of 'mem available' with 'mem free'
            df.filter(items=["mem free"]).plot.area(
                ax=ax1, color=self.colours["mem free"]
            )
            chatch = ax1.collections[0]
            chatch.set_label("mem cached")

        chatch.set_facecolor(self.colours["mem free"])
        chatch.set_edgecolor(self.colours["mem used"])
        # hatches = [".", "/", "\\", None, "\\\\", "*"]
        chatch.set_hatch("//")

        df.filter(items=["swap free"]).plot(
            ax=ax1, color=self.colours["swap free"], lw=3
        )

        self.common_ax1(figman, ax1)

        l1 = ax1.legend(loc="upper right", title="memory")
        l1.set_draggable(True)
        ax1.set_ylabel(f"mem ({self.mem_unit})")

    # -------------------------------------------------------------------------
    # Draw the graph of Processes of Interest (POI) using the given DataFrame

    def graph_poi(
        self,
        figman,
        df,
        ax,
        title,
        *,
        x_bounds=None,
        mem_bounds=None,
        single_core=None,
        overview: bool = False,  # pylint: disable=unused-argument
    ):
        max_cpu = 100
        max_mem = None

        # Convenience aliasing
        plot_cpu_lines = self.config.plot_poi_cpu_lines
        plot_cpu_sum = self.config.plot_poi_cpu_sum
        plot_mem_lines = self.config.plot_poi_mem_lines
        plot_mem_sum = self.config.plot_poi_mem_sum

        if (plot_mem_lines or plot_mem_sum) and self.config.include_process_mem:
            ax_cpu = ax.twinx()
            ax_mem = ax
        else:
            ax_cpu = ax
            ax_mem = ax.twinx()

        figman.ax_name_map[ax_cpu] = "ax_cpu"
        figman.ax_name_map[ax_mem] = "ax_mem"

        if (
            (plot_cpu_lines or plot_cpu_sum)
            and self.config.include_process_cpu
            and (plot_mem_lines or plot_cpu_sum)
            and self.config.include_process_mem
        ):
            figman.ax_pairs.append(ax_cpu, ax_mem)

        # ---------------------------------------------------------------------

        def style_line(
            ax, index, colour, alpha, linestyle, marker=None, mark_every=None
        ):
            line = ax.get_lines()[index]
            line.set_color(colour)
            line.set_alpha(alpha)
            line.set_linestyle(linestyle)
            if marker is None:
                marker = ""
            line.set_marker(marker)
            if mark_every is None:
                mark_every = 10
            line.set_markevery(mark_every)

        # ---------------------------------------------------------------------

        def max_cpu_fu(column_name):
            max_cpu = df[column_name].max()
            if max_cpu > 100:
                max_cpu = 100 * math.ceil((max_cpu + 0.1) / 100.0)
            else:
                max_cpu = 110
            return max_cpu

        # ---------------------------------------------------------------------

        def max_mem_fu(column_name):
            max_mem = df[column_name].max()
            return 10 * math.ceil((max_mem + 0.1) / 10.0)

        # ---------------------------------------------------------------------

        def handle_data(
            df,
            ax,
            separate_cores,
            plot_data_lines,
            plot_summary,
            plot_at_all,
            mode,
            summary_line_style,
            max_fu,
            max_fu_default,
            x_bounds,
        ):
            plotted = False
            if (plot_data_lines or plot_summary) and plot_at_all:
                summary_title = f"poi {mode} sum - {mode}"
                if plot_summary and not separate_cores:
                    # Create summary column if not already present
                    if summary_title not in df.columns.to_list():
                        summary = self.data.poi_df.filter(regex=f" - {mode}$").sum(
                            axis=1
                        )
                        df.insert(0, summary_title, summary)

                # Select columns by regex
                if not plot_data_lines:
                    regex = f"^{summary_title}$"
                else:
                    regex = f"- {mode}$"

                # Strip trailing category from names then plot
                def stripper(x):
                    return x[:-6] if x[-6:] == f" - {mode}" else x

                df = df.filter(regex=regex)
                if not df.empty:
                    df.rename(columns=stripper).plot(ax=ax, xlim=x_bounds)
                    plotted = True
                ax.set_ylabel(f"{mode} (%)")
                self.style_lines(ax)

                # Override summary line
                if plot_summary and not separate_cores:
                    colour, alpha, linestyle, marker, mark_every = summary_line_style
                    style_line(ax, 0, colour, alpha, linestyle, marker, mark_every)
                    return (plotted, max_fu(summary_title))

            return (plotted, max_fu_default)

        # ---------------------------------------------------------------------

        total_markers = 7.5
        mark_every = int(len(df) / total_markers)
        alpha = 0.33
        cpu_summary_line_style = (
            "mediumvioletred",
            alpha,
            (1, (1, 2, 1, 3)),
            "$c$",
            mark_every,
        )
        mem_summary_line_style = (
            "dodgerblue",
            alpha,
            (0, (2, 6, 2, 2)),
            "$m$",
            mark_every,
        )

        cpu_plotted, max_cpu = handle_data(
            df,
            ax_cpu,
            x_bounds is not None,
            plot_cpu_lines,
            plot_cpu_sum,
            self.config.include_process_cpu,
            "cpu",
            cpu_summary_line_style,
            max_cpu_fu,
            100 if single_core else 110,
            x_bounds,
        )

        mem_plotted, max_mem = handle_data(  # pylint: disable=unused-variable
            df,
            ax_mem,
            x_bounds is not None,
            plot_mem_lines,
            plot_mem_sum,
            self.config.include_process_mem,
            "mem",
            mem_summary_line_style,
            max_mem_fu,
            None,
            x_bounds,
        )

        # Handle legends
        l_mem_cuckoo = None

        # Handle mem
        if (plot_mem_lines or plot_mem_sum) and self.config.include_process_mem:
            # ax_mem's legend shouldn't be overwritten by lines on ax_cpu
            # Sadly they are being overwritten, so ensure they're not by adding
            # them to ax_cpu
            if (
                (plot_cpu_lines or plot_cpu_sum)
                and self.config.include_process_cpu
                and cpu_plotted
            ):
                handles, labels = ax_mem.get_legend_handles_labels()
                # Remove old legend's artists from drawing tree to avoid
                # bitching about artist reuse
                # Note: doesn't delete legend object
                old_l_mem = ax_mem.legend()
                old_l_mem.remove()
                l_mem_cuckoo = plt.legend(
                    handles, labels, loc="upper left", title="mem"
                )

            else:
                ax_mem.legend(loc="upper left", title="mem")
                ax_cpu.set_visible(False)

                l_mem = ax_mem.get_legend()
                # WARNING: accessing internal mpl details here
                label = (
                    l_mem._legend_title_box._text  # pylint: disable=protected-access
                )
                figman.map_legend_lines(ax_mem, label, l_mem)
                l_mem.set_draggable(True)
                ax_mem.xaxis.set_visible(True)
                ax_mem.patch.set_visible(True)

        # Handle cpu
        if (plot_cpu_lines or plot_cpu_sum) and self.config.include_process_cpu:
            l_cpu = ax_cpu.legend(loc="upper right", title="cpu")
            # WARNING: accessing internal mpl details here
            label = l_cpu._legend_title_box._text  # pylint: disable=protected-access
            figman.map_legend_lines(ax_cpu, label, l_cpu)
            l_cpu.set_draggable(True)

            if (
                not plot_mem_lines and not plot_mem_sum
            ) or not self.config.include_process_mem:
                ax_mem.set_visible(False)

        if l_mem_cuckoo is not None:
            ax_cpu.add_artist(l_mem_cuckoo)
            figman.register_legend(ax_cpu, "cuckoo", l_mem_cuckoo)
            # WARNING: accessing internal mpl details here
            label = (
                l_mem_cuckoo._legend_title_box._text  # pylint: disable=protected-access
            )
            figman.map_legend_lines(ax_mem, label, l_mem_cuckoo)
            l_mem_cuckoo.set_draggable(True)

        # Handle furniture
        ax_cpu.set_title(title)
        ax_mem.set_title(title)

        self.common_ax1(figman, ax_mem)
        self.common_ax2(figman, ax_cpu)

        if x_bounds is None:
            x_bounds = (df.head(1).index[0], df.tail(1).index[0])
        ax_cpu.set_xlim(x_bounds)

        ax_cpu.set_ybound(lower=0, upper=max_cpu)

        if mem_bounds is not None:
            min_mem, max_mem = mem_bounds
            ax_mem.set_ybound(lower=min_mem, upper=max_mem)
        elif max_mem is not None:
            ax_mem.set_ybound(lower=0, upper=max_mem)

    # -------------------------------------------------------------------------
    # Handle progress window when creating graph

    def dispense_graph(
        self, title, figman_name, setup, generate_figman, use_progress_window
    ):
        if figman_name in self.fig_manager:
            self.fig_manager[figman_name].show()
        else:

            def create_graph(self):
                figman = generate_figman()

                figman.setup_graphing(setup)

                if use_progress_window:
                    self.progress_window.hide()

                self.fig_manager[figman_name] = figman

            if use_progress_window:
                self.progress_window.update_status(f"preparing '{title}'")
                self.progress_window.show()
                self.progress_window.root.after(100, create_graph, self)
            else:
                create_graph(self)

    # -------------------------------------------------------------------------
    # Draw the requested graph from the Big Four overview graphs in its own Fig

    def graph_by_overview_ordinal(self, n, use_progress_window: bool = False):
        figman_name = f"overview_{n}"

        title = self.ordinal_to_cartesian_map(n)["title"]

        def setup(figman):
            ax = (
                figman.plots
            )  # Note necessary absence of cartesian indexing for single subplot
            self.graph_map[title]["fn"](
                figman,
                self.graph_map[title]["data"],
                ax,
                figman.subtitle,
                overview=False,
            )

        def generate_figman():
            return FigManager(
                figman_name,
                self,
                self.title(title),
                self.window_size,
                1,
                1,
            )

        self.dispense_graph(
            title.partition("\n")[0],
            figman_name,
            setup,
            generate_figman,
            use_progress_window,
        )

    # -------------------------------------------------------------------------
    # Draw the cpu data in separate plots for each CPU core

    def graph_cpu_per_cpu(self, use_progress_window: bool = False):
        figman_name = "cpu_by_cpu"
        title = "cpu data by cpu core"

        # Find the nearest integer square that will fit the plots
        sqrt = math.ceil(math.sqrt(int(self.cores)))

        # Account for this possibly being a row larger than needed
        excess_rows = 0
        if (sqrt * sqrt) > (self.cores + sqrt - 1):
            excess_rows = 1

        def setup(figman):
            min_timestamp = self.data.poi_df.head(1).index[0]
            max_timestamp = self.data.poi_df.tail(1).index[0]

            for core in range(self.cores):
                if self.cores < 3:
                    ax = figman.plots[core]
                else:
                    x = int(core / sqrt)
                    y = core % sqrt

                    ax = figman.plots[x][y]
                df = self.data.cpus_df.filter(regex=f"^cpu{core}")

                self.graph_cpus(
                    figman,
                    df,
                    ax,
                    f"core {core}",
                    x_bounds=(min_timestamp, max_timestamp),
                    force_single_core=core,
                )

        def generate_figman():
            return FigManager(
                figman_name,
                self,
                self.title(title),
                self.window_size,
                sqrt - excess_rows,
                sqrt,
            )

        self.dispense_graph(
            title.partition("\n")[0],
            figman_name,
            setup,
            generate_figman,
            use_progress_window,
        )

    # -------------------------------------------------------------------------
    # Draw the Processes of Interest in separate plots for each CPU core

    def graph_poi_per_cpu(self, use_progress_window: bool = False):
        figman_name = "poi_by_cpu"
        title = "poi by cpu core"

        # Find the nearest integer square that will fit the plots
        sqrt = math.ceil(math.sqrt(int(self.cores)))

        # Account for this possibly being a row larger than needed
        excess_rows = 0
        if (sqrt * sqrt) > (self.cores + sqrt - 1):
            excess_rows = 1

        def setup(figman):
            min_timestamp = self.data.poi_df.head(1).index[0]
            max_timestamp = self.data.poi_df.tail(1).index[0]

            max_mem = 0
            for core in range(self.cores):
                max_mem = max(
                    max_mem,
                    self.data.core_dfs[core].filter(regex=" - mem$").max().max(),
                )

            for core in range(self.cores):
                if self.cores < 3:
                    ax = figman.plots[core]
                else:
                    x = int(core / sqrt)
                    y = core % sqrt
                    ax = figman.plots[x][y]
                self.graph_poi(
                    figman,
                    self.data.core_dfs[core],
                    ax,
                    f"core {core}",
                    x_bounds=(min_timestamp, max_timestamp),
                    mem_bounds=(0, max_mem),
                    single_core=core,
                )

        def generate_figman():
            return FigManager(
                figman_name,
                self,
                self.title(f"{title}\n{self.config.poi_categories}"),
                self.window_size,
                sqrt - excess_rows,
                sqrt,
                subtitle=True,
            )

        self.dispense_graph(
            title.partition("\n")[0],
            figman_name,
            setup,
            generate_figman,
            use_progress_window,
        )

    # -------------------------------------------------------------------------
    # Draw the four overview graphs on a single Fig

    def graph_overview(self, use_progress_window: bool = False):
        figman_name = "overview"
        fig_title = "overview"

        def setup(figman):
            graph_index = 1
            for (x, y, title) in zip([0, 0, 1, 1], [0, 1, 0, 1], self.graph_map.keys()):
                ax = figman.plots[x][y]
                self.graph_map[title]["fn"](
                    figman,
                    self.graph_map[title]["data"],
                    ax,
                    f"({str(graph_index)}) {title}",
                    overview=True,
                )
                graph_index += 1

        def generate_figman():
            return FigManager(
                figman_name,
                self,
                self.title(fig_title),
                self.window_size,
                2,
                2,
            )

        self.dispense_graph(
            fig_title,
            figman_name,
            setup,
            generate_figman,
            use_progress_window,
        )

    # -------------------------------------------------------------------------
    # Call specified method on all the figs, the specified one, or the most
    # recently created one.

    def figs_foo(self, func, all_figs: bool, name: str = None):
        if self.fig_manager:
            figs = list(self.fig_manager.values())
            if name is not None:
                figs = next(filter(lambda x: x == name, figs))

            if figs:
                to_do_list = figs if all_figs else [figs[-1]]
                for figman in to_do_list:
                    if figman:
                        func(figman)

    # -------------------------------------------------------------------------
    # Save pngs of all the figs, the specified one, or the most recently
    # created one.

    def save_figs(self, all_figs: bool = True, name: str = None):
        self.figs_foo(FigManager.save, all_figs, name)

    # -------------------------------------------------------------------------
    # Close all the figs, the specified one, or the most recently created one.

    def close_figs(self, all_figs: bool = True, name: str = None):
        self.figs_foo(FigManager.close, all_figs, name)
        self.close_check()

    # -------------------------------------------------------------------------
    # FigManagers call this when closing to exit the app if they were the last one

    def close_check(self):
        if not self.fig_manager and self.at_close is not None:
            self.at_close()

    # -------------------------------------------------------------------------
    # Main function for setting things up and running

    def doit(self, at_showtime, at_close):
        self.at_close = at_close

        override_rcParams()

        for (x, y, title) in zip([0, 0, 1, 1], [0, 1, 0, 1], self.graph_map.keys()):
            self.cartesian_map[x][y] = {
                "title": title,
                "fn": self.graph_map[title]["fn"],
            }

        if len(self.config.which_graphs) > 0:
            count = 0

            for c in self.config.which_graphs:
                if c.isnumeric():
                    i = int(c)
                    if i == 0:
                        self.graph_overview()
                        count += 1

                    elif 1 <= i <= 4:
                        self.graph_by_overview_ordinal(i - 1)
                        count += 1

                    else:
                        warn("'-g' takes numbers from 0 to 4.")

                elif c == "c":
                    if self.cores > 1 and len(self.data.core_dfs) > 0:
                        self.graph_poi_per_cpu()
                        count += 1
                    else:
                        warn("No multi-core data available to plot POI by CPU core.")

                elif c == "C":
                    if self.cores > 1:
                        self.graph_cpu_per_cpu()
                        count += 1
                    else:
                        warn("No multi-core data available to plot CPU data by core.")

                elif c == "p":
                    if count > 0:
                        self.save_figs(all_figs=False)

                elif c == "P":
                    if count > 0:
                        self.save_figs()

                elif c == "q":
                    if count > 0:
                        self.close_figs(all_figs=False)
                        if count > 1:
                            count -= 1
                        else:
                            break
                    else:
                        break

                elif c == "Q":
                    if count > 0:
                        self.close_figs()
                    break

                else:
                    die(f"The character '{c}' doesn't represent a graph.")

        else:
            self.graph_overview()

        at_showtime()
        plt.show()


# -----------------------------------------------------------------------------
# vi: sw=4:ts=4:et
