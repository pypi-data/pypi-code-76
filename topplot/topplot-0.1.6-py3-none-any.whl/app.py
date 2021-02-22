# pylint: disable=no-member

import os
import pathlib
import re
import sys
import tempfile

from .config import Config
from .grapher import Grapher
from .re_variants import Re_Variants
from .progress_window import ProgressWindow
from .tempfile import (
    CpuFiles,
    dataframe_from_process_graph_data,
    from_csv,
    write_datafile,
)
from .topndict import TopNDict2
from .utils import dhms_to_sec, warn, info

# ------------------------------------------------------------------------------

CPU_COLUMNS = ["user", "system", "nice", "idle", "wait", "hw_irq", "sw_irq"]
MUSTHAVE_COLUMNS = ["%CPU", "COMMAND", "%MEM", "PID"]

# ------------------------------------------------------------------------------


class App:
    class Dataframes:
        def __init__(self):
            self.cpus_df = None
            self.tasks_df = None
            self.poi_df = None
            self.mem_df = None
            self.core_dfs = None

    def __init__(self, version):
        self.has_cpu_column = False
        self.has_cpu_rows = False

        # Some versions of top have values that other don't
        # So far it's either mem_cached or mem_available
        self.mem_cached_or_available = "mem_cached"
        self.mem_unit = "KiB"

        self.data = App.Dataframes()

        self.cores = 1
        self.highest_cpuid = None
        self.top_entries = []
        self.processes = {}
        self.processes_of_interest = {}
        self.re_process_header = None

        self.config = Config(self, version)

        self.setup_profiling()
        self.setup_regex()
        self.setup_tmpdir_and_files()

        self.progress_window = None if self.config.list_processes else ProgressWindow()

    # --------------------------------------------------------------------------

    def update_status(self, msg):
        if self.progress_window is not None:
            self.progress_window.update_status(msg)

    # --------------------------------------------------------------------------

    def setup_profiling(self):

        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from .profiler import Profiler
        except ImportError:
            # No profiler available, convert calls to empty stubs
            class DummyProfiler:
                def start(self, *args, **kwargs):
                    pass

                def start_new(self, *args, **kwargs):
                    pass

                def stop(self, *args, **kwargs):
                    pass

            self.profiler = DummyProfiler()
        else:
            tag1 = re.sub(  # strip everything after last '.'
                r"\.[^\.]+$", "", os.path.basename(self.config.toplog_filename)
            )

            if self.config.which_graphs is not None:
                tag1 = f"{tag1}_{self.config.which_graphs}"

            self.profiler = Profiler(
                self.config.profiling_tag is not None,
                tag1=tag1,
                tag2=self.config.profiling_tag,
            )

    # --------------------------------------------------------------------------
    # Set up for the temporary data files
    def setup_tmpdir_and_files(self):
        if self.config.tmpdir is None:
            self.tmpdir_context_manager = tempfile.TemporaryDirectory()
            self.tmpdir = self.tmpdir_context_manager.name
        else:
            self.tmpdir = self.config.tmpdir
            try:
                pathlib.Path(self.tmpdir).mkdir(mode=0o700, parents=True, exist_ok=True)
            except PermissionError as e:
                print(f"Can't create self.tmpdir: {e}")
                sys.exit(1)

        print(f"tmpdir: {self.tmpdir}")
        self.cpu_data_filename = os.path.join(self.tmpdir, "cpu.data")
        self.mem_data_filename = os.path.join(self.tmpdir, "mem.data")
        self.task_data_filename = os.path.join(self.tmpdir, "task.data")
        self.poi_combined_data_filename = os.path.join(self.tmpdir, "poi combined.data")
        self.poi_data_filename = os.path.join(self.tmpdir, "poi.data")

    # --------------------------------------------------------------------------

    def setup_regex(self):
        self.re_ignore_processes_regex = None
        if self.config.ignore_processes_regex:
            flags = 0
            if self.config.ignore_case:
                flags = re.IGNORECASE

            self.re_ignore_processes_regex = re.compile(
                self.config.ignore_processes_regex, flags
            )

        # ----------------------------------------------------------------------
        # Different versions of top require slightly different handling
        #
        # This is being handled by setting variables when what parses (!) for version
        # detection occurs.
        #
        # This is performed by optionally passing tuples of:
        #    ((var1_name, var1_value), (varN_name, varN_value))
        # in with regexes to Re_Variants instances.

        # ----------------------------------------------------------------------
        # Precompile regexps
        #
        # The group names, i.e the "word" in (?P<word>pattern), are used later
        # on as dictionary keys

        # top - 06:40:46 up 0 min,  0 users,  load average: 20.84, 5.41, 1.83
        self.re_top = re.compile(
            r"^top - (?P<timestamp>[^ ]+) .*load average: (?P<load_average>[0-9.]+), .*"
        )

        scope = locals()  # pylint: disable=used-before-assignment

        # Tasks: 301 total,  23 running, 209 sleeping,   0 stopped,   0 zombie
        self.re_tasks = Re_Variants(
            "re_tasks",
            re.compile(
                r"^Tasks: (?P<task_total>[0-9]+) total, +(?P<task_running>[0-9]+)"
                r" running,"
                r" +(?P<task_sleeping>[0-9]+) sleeping, +(?P<task_stopped>[0-9]+)"
                r" stopped,"
                r" +(?P<task_zombie>[0-9]+) zombie"
            ),
        )

        # Threads: 1529 total,   4 running, 1525 sleeping,   0 stopped,   0 zombie
        self.re_tasks.append(
            re.compile(
                r"^Threads: (?P<task_total>[0-9]+) total, +(?P<task_running>[0-9]+)"
                r" running,"
                r" +(?P<task_sleeping>[0-9]+) sleeping, +(?P<task_stopped>[0-9]+)"
                r" stopped,"
                r" +(?P<task_zombie>[0-9]+) zombie"
            ),
            (("self.config.threads_not_tasks", "True"),),
            scope=scope,
        )

        # Cpu(s): 51.8%us, 28.7%sy,  0.5%ni, 13.9%id,  1.4%wa,  0.0%hi,  3.7%si,  0.0%st
        self.re_cpu = re.compile(
            r"^%?Cpu(\(s\)|(?P<cpu_id>[0-9]+) +): *(?P<cpu_user>[0-9.]*)[% ]us,"
            r" *(?P<cpu_system>[0-9.]+)[% ]sy, *(?P<cpu_nice>[0-9.]+)[% ]ni,"
            r" *(?P<cpu_idle>[0-9.]+)[% ]id, *(?P<cpu_wait>[0-9.]+)[% ]wa,"
            r" *(?P<cpu_hw_irq>[0-9.]+)[% ]hi, *(?P<cpu_sw_irq>[0-9.]+)[% ]si,"
            r" *(?P<cpu_steal>[0-9.]+)[% ]st"
        )

        # Mem:   4046364k total,  2847408k used,  1198956k free,    37528k buffers
        self.re_mem = Re_Variants(
            "re_mem",
            re.compile(
                r"^Mem: +(?P<mem_total>[0-9]+)k total, +(?P<mem_used>[0-9]+)k used,"
                r" +(?P<mem_free>[0-9]+)k free, +(?P<mem_buffers>[0-9]+)k buffers"
            ),
        )

        # Swap:  2047996k total,        0k used,  2047996k free,  1468792k cached
        self.re_swap = Re_Variants(
            "re_swap",
            re.compile(
                r"^Swap: +(?P<swap_total>[0-9]+)k total, +(?P<swap_used>[0-9]+)k used,"
                r" +(?P<swap_free>[0-9]+)k free, +(?P<mem_cached>[0-9]+)k cached"
            ),
        )

        for unit in ["K", "M", "G", "T", "P", "E"]:
            # <unit>iB Mem : 15653.4 total,  6178.4 free,  7285.0 used,  2189.9 buff/cache
            self.re_mem.append(
                re.compile(
                    rf"^{unit}iB Mem : +(?P<mem_total>[.0-9]+) total,"
                    r" +(?P<mem_free>[.0-9]+)"
                    r" free, +(?P<mem_used>[.0-9]+) used, +(?P<mem_buffers>[.0-9]+)"
                    r" buff/cache"
                ),
                (("self.mem_unit", f"{unit}iB"),),
                scope=scope,
            )

            # <unit>MiB Swap: 15792.0 total, 10146.5 free,  5645.5 used.  7242.8 avail Mem
            self.re_swap.append(
                re.compile(
                    rf"^{unit}iB Swap: +(?P<swap_total>[.0-9]+) total,"
                    r" +(?P<swap_free>[.0-9]+)"
                    r" free, +(?P<swap_used>[.0-9]+) used\. +(?P<mem_available>[.0-9]+)"
                    r" avail"
                ),
                (("self.mem_cached_or_available", "mem_available"),),
                scope=scope,
            )

        # 2019-01-31 06:40:41:709
        self.re_timestamp = re.compile(r"^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d:\d\d\d$")

        self.re_process = None
        self.re_process_header = None

    # --------------------------------------------------------------------------

    def generate_re_process(self, line):
        if self.config.threads_not_tasks:
            # Command *must* be the rightmost column
            command_pattern = r"(?P<commandline>(?P<command>.+))"
        else:
            # Command shouldn't contain spaces
            command_pattern = r"(?P<commandline>(?P<command>[^ ]+).*)"

        columnheader_to_regex = {
            "%CPU": r"(?P<cpu>[\d.]+)",
            "COMMAND": command_pattern,
            "%MEM": r"(?P<mem>[\d.]+[mg]?)",
            "NI": r"(?P<nice>[\d-]+)",
            "P": r"(?P<cpuid>\d+)",
            "PID": r"(?P<pid>[0-9]+)",
            "PR": r"(?P<priority>[\drRtT-]+)",
            "RES": r"(?P<res>[\d.]+[mg]?)",
            "S": r"(?P<state>[DIRSTtXZ]+)",
            "SHR": r"(?P<shr>[\d.]+[mg]?)",
            "SWAP": r"(?P<swap>[\d.]+[mg]?)",
            "TIME+": r"(?P<time>[\d:.]+)",
            "USER": r"(?P<user>[\w+-]+)",
            "VIRT": r"(?P<virt>[\d.]+[mg]?)",
        }

        found = {}
        header_pattern = "^"
        process_pattern = "^"
        prespace = " *"

        line = line.rstrip("\n")

        for columnheader in re.findall(r"([^ ]+)", line):
            found[columnheader] = True
            header_pattern += prespace + columnheader.replace("+", "\\+")

            if columnheader in columnheader_to_regex:
                process_pattern += prespace + columnheader_to_regex[columnheader]
                prespace = " +"
            else:
                print(
                    ">INFO: header line contains unhandled columnheader"
                    f" '{columnheader}'",
                    file=sys.stderr,
                )
                process_pattern += prespace + r"(?:[^ ]+)"

        header_pattern += r"\s*$"
        process_pattern += r"$"

        missing = []

        for musthave in MUSTHAVE_COLUMNS:
            if musthave not in found:
                missing.append(musthave)

        if len(missing) > 0:
            print(
                f">ERR: missing essential process column(s): {missing}\nAborting.",
                file=sys.stderr,
            )
            sys.exit(1)

        return (
            header_pattern,
            re.compile(header_pattern),
            re.compile(process_pattern),
        )

    # --------------------------------------------------------------------------

    def parse(self):
        self.update_status(f"parsing '{os.path.basename(self.config.toplog_filename)}'")

        class ParseContext:
            def __init__(self):
                self.cpu_id = None
                self.current_entry = {}
                self.line_count = 0
                self.first_secs = None
                self.prev_secs = None
                self.re_process = None

        context = ParseContext()

        # Encoding set to ISO-8859-1 in response to 0xFF char used in a threadname (!)
        # causing topplot to die horribly. Will this have knock on effects in non-ASCII
        # environments?

        with open(self.config.toplog_filename, encoding="ISO-8859-1") as top_log:

            for (
                line
            ) in top_log:  # Swapping over to .readlines(10000): leads to Bad Things
                context.line_count += 1
                line = line.rstrip()
                if not line:
                    continue

                # print(f"{context.line_count}: len: {len(line)}", file=sys.stderr)

                top_line_match = self.re_top.match(line)

                if top_line_match:
                    self.parse_header(
                        top_log, context, top_line_match,
                    )
                else:
                    #  There won't be a current_entry if the start of the file
                    #  is corrupted or we're skipping content until
                    #  self.config.start_time
                    if context.current_entry:
                        # Expecting a process line at this point
                        # print(f"{context.line_count} : >{line}<", file=sys.stderr)
                        process_match = context.re_process.match(line)

                        if process_match:
                            self.parse_process_line(
                                line, context.current_entry["timestamp"], process_match
                            )

        if context.current_entry:  # stash the final entry
            self.top_entries.append(context.current_entry)

        # Rather than expend effort on max() calls, assume that the header is sorted
        self.highest_cpuid = context.cpu_id

    # --------------------------------------------------------------------------

    def parse_header(self, top_log, context, header_match):
        # starting a new entry, so stash previous one
        if context.current_entry:
            self.top_entries.append(context.current_entry)

        groupdict = header_match.groupdict()

        try:
            assert groupdict["timestamp"] is not None
        except AssertionError:
            print(f"ERR: Expected a timestamp field at line {context.line_count} !?")
            return

        context.current_entry = groupdict

        # Handle start/stop times
        current_secs = dhms_to_sec(context.current_entry["timestamp"])

        if context.first_secs is None:
            context.first_secs = current_secs

        if context.prev_secs is not None:
            # Handle midnight wrapping
            # Not sure that
            while current_secs < context.prev_secs:
                current_secs += 24 * 60 * 60

        # Convert to play nicely with matplotlib
        context.current_entry["timestamp"] = current_secs

        context.prev_secs = current_secs

        if self.config.start_time:
            if isinstance(self.config.start_time, str):
                offset = dhms_to_sec(self.config.start_time[1:])

                self.config.start_time = current_secs + offset

            if current_secs < self.config.start_time:
                context.current_entry = None
                return

        if self.config.stop_time:
            if isinstance(self.config.stop_time, str):
                offset = dhms_to_sec(self.config.stop_time[1:])

                if self.config.stop_time[0:1] == "+":
                    self.config.stop_time = current_secs + offset

                elif self.config.stop_time[0:1] == "<":
                    self.config.stop_time = context.first_secs + offset

            if current_secs >= self.config.stop_time:
                context.current_entry = None
                return

        # By default the header lines are of structure:
        #   Tasks:
        #   Cpu(s):
        #   Mem:
        #   Swap:
        #
        #   PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
        #
        # But Cpu can be aggregate or split out by core, and the process header
        # line is mutable

        have_all_expected_header_lines = True
        pull_line = True
        line = ""
        for regex in [
            self.re_tasks,
            self.re_cpu,
            self.re_mem,
            self.re_swap,
        ]:
            if pull_line:
                line = top_log.readline()
            pull_line = True

            if line:
                context.line_count += 1
                match = regex.match(line)
                if match:
                    if regex is self.re_cpu:
                        context.cpu_id = match.group("cpu_id")
                        if context.cpu_id is not None:
                            # Handle split out CPU info
                            self.has_cpu_rows = True
                            pull_line = False
                            while match:
                                context.line_count += 1
                                context.cpu_id = match.group("cpu_id")
                                temp_dict = match.groupdict()
                                for key in [
                                    "user",
                                    "system",
                                    "nice",
                                    "idle",
                                    "wait",
                                    "hw_irq",
                                    "sw_irq",
                                    "steal",
                                ]:
                                    temp_dict[
                                        f"cpu{context.cpu_id}_{key}"
                                    ] = temp_dict.pop("cpu_" + key)
                                context.current_entry.update(temp_dict)
                                line = top_log.readline()
                                match = regex.match(line)
                            context.line_count -= 1
                        else:
                            context.current_entry.update(match.groupdict())
                    else:
                        context.current_entry.update(match.groupdict())
                else:
                    have_all_expected_header_lines = False
                    print(
                        f">ERR: line {context.line_count}: >{line}<\n   :"
                        f" Unexpected match failure for {regex.pattern}",
                        file=sys.stderr,
                    )
            else:
                have_all_expected_header_lines = False

        if have_all_expected_header_lines:
            # Blank line
            line = top_log.readline()  # blank line
            if len(line) != 1:  # 1 for newline char
                print(
                    f">ERR: line {context.line_count}: >{line}<\nExpected a blank line"
                    " here.",
                    file=sys.stderr,
                )

            # Process header line
            line = top_log.readline()
            process_header_pattern = ""
            if not self.re_process_header:
                (
                    process_header_pattern,
                    self.re_process_header,
                    context.re_process,
                ) = self.generate_re_process(line)
                if " +P " in self.re_process_header.pattern:
                    self.has_cpu_column = True
                    if not self.has_cpu_rows:
                        print(
                            "Currently when tracking per process CPU core"
                            " use, topplot needs per core CPU information"
                            " too."
                        )
                        print(
                            "For more information see the 'Workaround'"
                            " section"
                            " here:"
                            " https://gitlab.com/eBardie/topplot/-/issues/11"
                        )
                        sys.exit(1)
            if not self.re_process_header.match(line):
                print(
                    f">ERR: line {context.line_count}: expected a process header"
                    f" line ({process_header_pattern}),\n got>{line}<",
                    file=sys.stderr,
                )

            context.line_count += 2

    # --------------------------------------------------------------------------

    def parse_process_line(self, line, timestamp, process_match):
        groupdict = process_match.groupdict()

        pid = process_match.group("pid")
        del groupdict["pid"]

        command = process_match.group("command")
        del groupdict["command"]

        # Just the basename please
        if command[0:1] == "/":
            slash = command.rfind("/")
            if slash > -1:
                command = command[slash + 1 :]

        if command == "" or len(command) == 0:
            print(f"WARN: command empty for line: {line}")

        # Skip this process if it matches the ignore regex and doesn't match
        # the POI regex
        if (
            self.re_ignore_processes_regex
            and self.re_ignore_processes_regex.match(command)
        ) and not (self.poi_regex and self.poi_regex.match(command)):
            return

        if command not in self.processes:
            self.processes[command] = {}

        if pid not in self.processes[command]:
            self.processes[command][pid] = {}
            self.processes[command][pid]["timestamps"] = {}

            # Storing at this point obviously won't cope with processes that
            # update their own ARGV[0]
            self.processes[command][pid]["commandline"] = groupdict["commandline"]

            if self.config.poi_acc_cpu:
                self.processes[command][pid]["acc_cpu"] = 0
            if self.config.poi_acc_mem:
                self.processes[command][pid]["acc_mem"] = 0
            if self.config.poi_peak_cpu:
                self.processes[command][pid]["max_cpu"] = 0
            if self.config.poi_peak_mem:
                self.processes[command][pid]["max_mem"] = 0

        # Bizarrely top can throw out reports where all processes' CPU column
        # entries are negative
        cpu_value = float(groupdict["cpu"])
        if cpu_value < 0:
            groupdict["cpu"] = str(cpu_value * -1)

        if self.config.poi_acc_cpu:
            self.processes[command][pid]["acc_cpu"] += float(groupdict["cpu"])

        if self.config.poi_acc_mem:
            self.processes[command][pid]["acc_mem"] += float(groupdict["mem"])

        if self.config.poi_peak_cpu:
            cpu = float(groupdict["cpu"])
            if cpu > self.processes[command][pid]["max_cpu"]:
                self.processes[command][pid]["max_cpu"] = cpu

        if self.config.poi_peak_mem:
            mem = float(groupdict["mem"])
            if mem > self.processes[command][pid]["max_mem"]:
                self.processes[command][pid]["max_mem"] = mem

        self.processes[command][pid]["timestamps"][timestamp] = groupdict

    # --------------------------------------------------------------------------
    # Early non-graphing output

    def list_processes(self):
        for command in sorted(self.processes.keys()):
            pids = []
            for pid in sorted(self.processes[command].keys()):
                if self.config.list_processes >= 2:
                    print(
                        f"{command} [{pid}]"
                        f" {self.processes[command][pid]['commandline']}"
                    )
                else:
                    pids.append(pid)

            if self.config.list_processes == 0:
                print(f"{command}")
            elif self.config.list_processes == 1:
                print(f"{command} x{len(pids)} {pids}")

    # --------------------------------------------------------------------------

    def write_datafile(self, filename, source, keys):
        if not self.config.allow_write:
            return
        write_datafile(filename, source, keys)

    # --------------------------------------------------------------------------
    # Munge top's header info
    def munge_header_info(self):
        if self.highest_cpuid is None:
            cpu_keys = [
                "load_average",
                "cpu_user",
                "cpu_system",
                "cpu_nice",
                "cpu_idle",
                "cpu_wait",
                "cpu_hw_irq",
                "cpu_sw_irq",
                "cpu_steal",
            ]

        else:
            self.cores = int(self.highest_cpuid) + 1
            cpu_keys = ["load_average"]
            column_index = 3
            columns = CPU_COLUMNS
            if self.config.with_cpu_steal:
                columns.append("steal")
            for i in range(0, self.cores):
                for column in columns:
                    cpu_keys.append(f"cpu{i}_{column}")
                    column_index += 1

        self.write_datafile(self.cpu_data_filename, self.top_entries, cpu_keys)

        mem_keys = [
            "mem_used",
            "mem_free",
            "mem_buffers",
            self.mem_cached_or_available,
            "swap_free",
        ]

        self.write_datafile(self.mem_data_filename, self.top_entries, mem_keys)

        task_keys = ["task_running", "task_sleeping", "task_stopped", "task_zombie"]

        self.write_datafile(self.task_data_filename, self.top_entries, task_keys)

    # --------------------------------------------------------------------------
    # Munge top's poi info
    def munge_poi_info(self):
        acc_cpu = None
        acc_mem = None
        peak_cpu = None
        peak_mem = None

        # Keep track of top N lists on request
        if self.config.poi_acc_cpu:
            acc_cpu = TopNDict2(
                self.config.poi_acc_cpu,
                "accumlated cpu",
                self.processes_of_interest,
                verbosity=self.config.verbosity,
            )

        if self.config.poi_acc_mem:
            acc_mem = TopNDict2(
                self.config.poi_acc_mem,
                "accumlated mem",
                self.processes_of_interest,
                verbosity=self.config.verbosity,
            )

        if self.config.poi_peak_cpu:
            peak_cpu = TopNDict2(
                self.config.poi_peak_cpu,
                "peak cpu",
                self.processes_of_interest,
                verbosity=self.config.verbosity,
            )

        if self.config.poi_peak_mem:
            peak_mem = TopNDict2(
                self.config.poi_peak_mem,
                "peak mem",
                self.processes_of_interest,
                verbosity=self.config.verbosity,
            )

        # Loop over all processes, keeping tabs on top N lists and filtering for POI
        for command in self.processes:
            for pid in self.processes[command]:
                # Update top-N lists if required
                if acc_cpu:
                    acc_cpu.append(
                        command, pid, self.processes[command][pid]["acc_cpu"]
                    )

                if acc_mem:
                    acc_mem.append(
                        command, pid, self.processes[command][pid]["acc_mem"]
                    )

                if peak_cpu:
                    peak_cpu.append(
                        command, pid, self.processes[command][pid]["max_cpu"]
                    )

                if peak_mem:
                    peak_mem.append(
                        command, pid, self.processes[command][pid]["max_mem"]
                    )

                # Run main filters
                for timestamp in self.processes[command][pid]["timestamps"].keys():
                    if self.config.filterfoo(command, pid, timestamp):
                        if command not in self.processes_of_interest:
                            if command == "":
                                warn(
                                    f"Adding empty command (?) for pid {pid} at"
                                    f" {timestamp}"
                                )
                            self.processes_of_interest[command] = {}

                        self.processes_of_interest[command][pid] = True
                        continue

        # Extract POI from top-N lists if required. Also dump info to stdout on request
        if self.config.poi_acc_cpu:
            acc_cpu.complete()

        if self.config.poi_acc_mem:
            acc_mem.complete()

        if self.config.poi_peak_cpu:
            peak_cpu.complete()

        if self.config.poi_peak_mem:
            peak_mem.complete()

    # ------------------------------------------------------------------------------
    # Munge data for processes of interest to its file(s)

    def munge_poi_data_to_files(self):

        data_by_core = CpuFiles(
            self.config, self.tmpdir, self.poi_combined_data_filename, self.cores
        )

        with open(self.poi_data_filename, "w") as poi_data:
            keys = ["cpu", "mem"]

            # Data
            block_index = -1

            for command in self.processes_of_interest:
                if command == "":
                    warn("Skipping empty command (?)")
                    continue

                pids = self.processes_of_interest[command]

                for pid in pids:
                    if not self.processes[command][pid]["timestamps"]:
                        warn(f"Unexpected lack of timestamps for {command}:{pid}")
                        continue

                    block_index += 1

                    if len(pids) > 1:
                        qualified_command = f"{command}:{pid}"
                    else:
                        qualified_command = f"{command}"

                    # Header
                    line = "timestamp"
                    for key in keys:
                        key = key.replace("_", " ")
                        line = f'{line} "{qualified_command} - {key}"'

                    header = f"\n{line}\n"
                    poi_data.write(header)

                    # Data
                    for timestamp in self.processes[command][pid]["timestamps"].keys():
                        line = f"{timestamp}"
                        for key in keys:
                            line = (
                                f"{line}"
                                f" {self.processes[command][pid]['timestamps'][timestamp][key]}"
                            )
                        txt = line + "\n"
                        poi_data.write(txt)
                        if self.has_cpu_column:
                            core = int(
                                self.processes[command][pid]["timestamps"][timestamp][
                                    "cpuid"
                                ]
                            )

                            # Write data to split out file
                            data_by_core.write(core, header, txt)

                            # Update per core aggregate pile(s) as appropriate
                            if self.config.plot_poi_cpu_sum:
                                data_by_core.add_poi_cpu(
                                    core,
                                    timestamp,
                                    float(
                                        self.processes[command][pid]["timestamps"][
                                            timestamp
                                        ]["cpu"]
                                    ),
                                )

                            if self.config.plot_poi_mem_sum:
                                data_by_core.add_poi_mem(
                                    core,
                                    timestamp,
                                    self.processes[command][pid]["timestamps"][
                                        timestamp
                                    ]["mem"],
                                )

                    poi_data.write("\n")

                    if self.has_cpu_column:
                        data_by_core.seal_register()

            data_by_core.close()

    # --------------------------------------------------------------------------

    def prep_dataframes_from_files(self):
        self.update_status("prepping dataframes")
        self.data.cpus_df = from_csv(self.cpu_data_filename)
        self.data.tasks_df = from_csv(self.task_data_filename)
        self.data.poi_df = dataframe_from_process_graph_data(self.poi_data_filename)
        self.data.mem_df = from_csv(self.mem_data_filename)

        # Add extra column(s) for summary CPU info
        ns = [""] if self.cores == 1 else range(self.cores)
        for n in ns:
            self.data.cpus_df[f"cpu{n} exec"] = (
                self.data.cpus_df[f"cpu{n} system"]
                + self.data.cpus_df[f"cpu{n} user"]
                + self.data.cpus_df[f"cpu{n} nice"]
            )

        # Prep the poi-by-core data
        self.data.core_dfs = []
        if self.has_cpu_column and self.cores > 1:
            for core in range(self.cores):
                self.data.core_dfs.append(
                    dataframe_from_process_graph_data(
                        f"{self.tmpdir}/cpu{core}_process.data"
                    )
                )

    # --------------------------------------------------------------------------

    def produce_graphs(self, at_showtime, at_close):
        self.update_status("producing graphs")

        cpus_graph_title = "cpu data"
        tasks_graph_title = "task data"
        poi_graph_title = f"processes of interest\n{self.config.poi_categories}"
        mem_graph_title = "mem data"

        # Awkward initialize sequence to allow graph_map to reference grapher functions
        graph_map = {}

        graphs = Grapher(
            graph_map,
            self.config,
            self.data,
            self.cores,
            self.mem_unit,
            self.mem_cached_or_available,
            self.progress_window,
        )

        # Order here determines display order in overview figure
        graph_map[poi_graph_title] = {
            "fn": graphs.graph_poi,
            "fig": None,
            "data": self.data.poi_df,
        }
        graph_map[cpus_graph_title] = {
            "fn": graphs.graph_cpus,
            "fig": None,
            "data": self.data.cpus_df,
        }
        graph_map[mem_graph_title] = {
            "fn": graphs.graph_mem,
            "fig": None,
            "data": self.data.mem_df,
        }
        graph_map[tasks_graph_title] = {
            "fn": graphs.graph_tasks,
            "fig": None,
            "data": self.data.tasks_df,
        }

        graphs.doit(at_showtime, at_close)

    # --------------------------------------------------------------------------

    def run(self):
        self.profiler.start("parse")
        self.parse()

        if self.config.list_processes:
            self.list_processes()
            self.progress_window.hide()
            self.profiler.stop()
            return

        self.update_status("munging")
        self.munge_header_info()
        self.munge_poi_info()
        self.munge_poi_data_to_files()

        if len(self.processes_of_interest) < 1:
            info(
                "INFO: No processes of interest according to selection criteria:"
                f" {self.config.poi_categories}"
            )
            self.progress_window.hide()
            self.profiler.stop()
            return

        if self.config.do_graph:
            self.prep_dataframes_from_files()
            self.profiler.start_new("graph")
            self.produce_graphs(self.progress_window.hide, self.progress_window.destroy)
        else:
            self.progress_window.destroy()

        self.profiler.stop()


# ------------------------------------------------------------------------------
# vi: sw=4:ts=4:et:tw=0
