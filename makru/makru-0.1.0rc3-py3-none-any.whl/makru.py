from pathlib import Path
from makru.store import Store
from .yamlh import yaml_load, yaml_dump
from .plug import PlugBox
import os
import sys
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Tuple
import asyncio


class Panic(Exception):
    def __init__(self, message, *args) -> None:
        self.message = message
        super().__init__(message, *args)

    def __str__(self) -> str:
        return "panic: {}".format(self.message)


def panic(msg: str):
    """
    Panic program by `msg`
    """
    raise Panic(msg)


def true_or_panic(test: bool, msg: str):
    """
    If `test` is `False`, panic by `msg`
    """
    if not test:
        panic(msg)


def file_exists(path, go_panic=False, msg="could not found {it}."):
    """
    Check whether a file exists in `path`, return `True` if exists. If not, panic by `msg` if `go_panic` is `True`, otherwise return False.
    """
    if not os.path.exists(path):
        if go_panic:
            panic(msg.format(it=path))
        else:
            return False
    return True


class Depend(object):
    def __init__(self, d: str):
        self.name: str
        self.dtype: str
        self.version: Optional[str] = None
        self.path: Optional[str] = None
        if not d.startswith("@"):
            parts = d.split("@")
            self.name = parts[0]
            self.dtype = "direct"
            if len(parts) > 1:
                self.version = parts[1]
        else:
            # @(opt/path)
            self.dtype = "path"
            self.path = d[2:-1]

    def __repr__(self):
        if self.dtype == "direct":
            return "{} {}".format(
                self.name, self.version if hasattr(self, "version") else "*"
            )
        elif self.dtype == "path":
            return "@({})".format(self.path)
        else:
            return "Depend@{}".format({"type": self.type})


class CompilingDesc(object):
    def __init__(self, sandbox: "Sandbox", *, root: str, name: str, use: str, **kvargs):
        self.sandbox = sandbox
        self.config = kvargs
        self.root: str = root
        self.dependencies = list(
            map(self.make_depend_obj, kvargs.get("dependencies", []))
        )
        self.name: str = name
        self.type = kvargs.get("type", None)
        self.use = use
        self.action_arg = kvargs.get("action_arg", None)
        self.action_default_arg = kvargs.get("action_default_arg", None)

    @staticmethod
    def make_depend_obj(s):
        return Depend(s)

    @property
    def gvars(self) -> Dict[str, Any]:
        return self.sandbox.gconfig["vars"]

    def expand_path(self, path):
        return self.sandbox.expand_path(path)


class Sandbox(object):
    def __init__(self, confpath, **globalconf):
        self.plugbox = PlugBox()
        self.gconfig: Dict[str, Any] = globalconf
        self.confpath = os.path.realpath(confpath)
        file_exists(self.confpath, go_panic=True)
        self.root = os.path.split(os.path.realpath(confpath))[0]
        self.config = self.prepare_config(confpath)
        self.private_actions: Dict[str, function] = {}
        self._info_store: Store = None
        self._build_store: Store = None

    @property
    def info_store(self):
        if not self._info_store:
            self.init_info_store()
        return self._info_store

    def init_info_store(self):
        dir = str(Path(self.root) / ".makru")
        return self.make_store_under(dir, "info")

    @property
    def build_store(self):
        return self._build_store

    def set_build_store(self, store: Store):
        if self._build_store:
            panic(
                "build store could not be overrided, old: {}, new: {}".format(
                    self._build_store, store
                )
            )
        self._build_store = store

    @staticmethod
    def make_store_under(directory: str, name: str) -> Store:
        filename = "{}.sqlite3".format(name)
        dir_path = Path(directory)
        if not Path(directory).exists():
            dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / filename
        return Store(str(file_path))

    def add_private_action(self, name: str, action=None):
        """
        Add `action` as a private action called `name`.
        If `action` is `None`, return a warppeer.
        """
        true_or_panic(
            name.startswith("_"),
            "private action's name should be leaded by '_': {}".format(name),
        )
        if action:
            self.private_actions[name] = action
        else:

            def wrapper(f):
                self.add_private_action(name, f)
                return f

            return wrapper

    @staticmethod
    def prepare_config(confpath):
        with open(confpath, "r") as f:
            return yaml_load(f.read())

    def ready(self):
        self.plug_search()
        self.plugbox.runhook("on_sandbox_load", self)

    def plug_check_and_load(
        self, user_request: str, check="compile", panic_if_notfound=True
    ):
        """
        Check the attribute `check` in plugin `user_request`.
        Panic if `panic_if_notfound` is `True` and the plugin or the attribute is not found.
        Return plugin namespace.
        """
        if self.plugbox.exists(user_request):
            plugin = self.plugbox.load(user_request)
            if hasattr(plugin, check):
                return plugin
            else:
                panic(
                    "plugin {} requested in {} does not support {} hook".format(
                        user_request, self.confpath, check
                    )
                )
        else:
            if panic_if_notfound:
                panic(
                    "could not found plugin {} requested in {}, all plugins: {}, searched paths: {}".format(
                        user_request,
                        self.confpath,
                        self.plugbox.plugin_names(),
                        self.plugbox.searchpaths,
                    )
                )

    def plug_search(self):
        if "plugin_paths" in self.gconfig:
            for p in self.gconfig["plugin_paths"]:
                self.plugbox.searchpaths.append(self.expand_path(p))
        if "plugin_paths" in self.config:
            for p in self.config["plugin_paths"]:
                self.plugbox.searchpaths.append(self.expand_path(p))
        self.plugbox.searchpaths.append(self.expand_path("./makru/plugins"))

    def build_desc(self, *, action_default_arg=None):
        config = self.config
        config["root"] = self.root
        return CompilingDesc(self, action_default_arg=action_default_arg, **config)

    def compile(self):
        target_plugin = self.plug_check_and_load(self.config["use"])
        self.run_action_function(target_plugin.compile, self.build_desc())

    def get_actions_conf(self):
        return self.config.get("actions", {})

    @staticmethod
    def action_split(action_name: str) -> Tuple[str, Optional[str]]:
        parts = action_name.split("(")
        name = parts[0]
        if len(parts) < 2:
            return (name, None)
        darg = parts[1][:-1]
        return (name, darg)

    def is_action_exists(self, name):
        actions = self.get_actions_conf()
        target_action_s = actions.get(name, None)
        if target_action_s:
            parts = target_action_s.split(":")
            true_or_panic(
                len(parts) == 2,
                "action defined in wrong format, the right format is <plugin name>:<function name>, recviced is {}".format(
                    target_action_s
                ),
            )
            plugin_name = parts[0]
            function_name, default_arg = self.action_split(parts[1])
            plugin = self.plug_check_and_load(
                plugin_name, check=function_name, panic_if_notfound=False
            )
            if not plugin:
                return False
            return getattr(plugin, function_name, None) != None
        elif name in self.gconfig["bulitin_actions"]:
            return True
        elif name in self.private_actions:
            return True
        else:
            return False

    @staticmethod
    def run_action_function(f, *args, **kwargs):
        """Run function `f` which could return awaitable or other types.
        If the return value is awaitable, use `asyncio.run` to wait on it, and return the final value.
        Otherwise return the return value. 
        """
        result = f(*args, **kwargs)
        if isinstance(result, Awaitable):
            return asyncio.run(result)
        else:
            return result

    def run_action(self, name, arg=None):
        """
        Run (private or public) action called `name`.
        Return the return value of the action call.
        """
        actions = self.get_actions_conf()
        target_action_s = actions.get(name, None)
        if target_action_s:
            parts = target_action_s.split(":")
            true_or_panic(
                len(parts) == 2,
                "action defined in wrong format, the right format is <plugin name>:<function name>, recviced is {}".format(
                    target_action_s
                ),
            )
            plugin_name = parts[0]
            function_name, default_arg = self.action_split(parts[1])
            plugin = self.plug_check_and_load(plugin_name, check=function_name)
            actionf = getattr(plugin, function_name)
            return self.run_action_function(
                actionf,
                self.build_desc(action_default_arg=default_arg)
            )
        elif name in self.gconfig["bulitin_actions"]:
            actionf = self.gconfig["bulitin_actions"][name]
            return self.run_action_function(actionf, self.build_desc())
        elif name in self.private_actions:
            actionf = self.private_actions[name]
            return self.run_action_function(actionf, self.build_desc())
        else:
            panic("could not find action {}".format(name))

    def expand_path(self, s):
        """
        Expand the path `s` as if the `self.root` is the current working directory.
        """
        if s.startswith("./"):
            return os.path.join(self.root, s[2:])
        elif not s.startswith("/"):
            return os.path.join(self.root, s)
        else:
            return s


class OptionDescription(object):
    def __init__(
        self,
        *,
        plugin_name: Optional[str] = None,
        description: Optional[str] = None,
        multiple: bool=False,
        bool_value: bool=False,
        mix_into: Optional[str] = None
    ) -> None:
        self.plugin_name = plugin_name
        if mix_into and (not description):
            self.description = "alias for {}".format(mix_into)
        elif description:
            self.description = description
        if not self.description:
            self.description = "*NO DESCRIPTION*"
        assert not (
            multiple and bool_value
        )  # option could not accept multiple bool values
        assert not (
            mix_into and (multiple or bool_value)
        )  # mix_into means this option just a alias for the mixed variable
        self.bool_value = bool_value
        self.multiple = multiple
        self.mix_into = mix_into


class Makru(object):
    def __init__(self, arguments=None):
        self._autorun_compile = True
        self.arguments = arguments if arguments else sys.argv[1:]
        self.option_descriptions: Dict[str, OptionDescription] = {}
        root_config_path = self.search_config_path(self.arguments)
        if not root_config_path:
            root_config_path = "./makru.yaml"
        self.globalconfig = {
            "plugin_paths": [],
            "root_config_path": root_config_path,
            "bulitin_actions": {
                "compile": self.compile,
                "list_actions": self.list_actions,
            },
            "vars": {},
        }
        assert len(self.globalconfig["vars"]) == 0
        self.build_sandbox().plugbox.runhook("after_configuration_load", self)
        self.options = self.scanflags()
        self.globalconfig["vars"].update(self.options["vars"])

    def define_option(self, name: str, description: OptionDescription):
        if name in self.option_descriptions:
            panic(
                "{} have been exists in options. the old one is by {}, the new one is by {}".format(
                    name,
                    self.option_descriptions[name].plugin_name,
                    description.plugin_name,
                )
            )
        self.option_descriptions[name] = description
        if description.multiple:
            self.globalconfig["vars"][name] = []

    @classmethod
    def search_config_path(cls, arguments: List[str]):
        config_indexs: List[int] = []
        result: Optional[str] = None
        for i, option in zip(range(0, len(arguments)), arguments):
            if option.startswith("-F"):
                result = cls.correct_config_path(option[2:])
                config_indexs.append(i)
        if len(config_indexs) > 1:
            print("WARN there are multiple config paths, {} is picked".format(result))
        for v in list(
            map(lambda x: arguments[x], config_indexs)
        ):  # .remove also cause indexes changes, we need a "snapshot" of values
            arguments.remove(
                v
            )  # Every .pop() cause the change of indexes, so here use value to remove the element
        return result

    def show_helps(self):
        print(
            "{} [:<action> [<action_argument>] [...]] [-F<path>] [-C] [--<key>=<value> --<key> --!<key>...] [-h]".format(
                "makru"
            )
        )
        print(
            ":<action> [<action_argument>]",
            "set the <action> you want to call, optionally uses <action_argument> as argument",
        )
        print(
            "-F<path>",
            "use <path> as makru config file or project folder needed to find makru config",
        )
        print("-C", "start compile after the other operations were done")
        print("--<key>=<value>/<key>=<value>", "define variable <key> as <value>")
        print("--<key>", "means --<key>=true")
        print("--!<key>", "means --<key>=false")
        print("-h", "only show this message")
        if len(self.option_descriptions) > 0:
            print("")
            print("Options:")
            option_keys = list(self.option_descriptions.keys())
            option_keys.sort()
            for name in option_keys:
                optiond = self.option_descriptions[name]
                option_show: str = None
                option_description = optiond.description
                if optiond.multiple:
                    option_show = "--{name}=<value>/{name}=<value> [--{name}=<value>/{name}=<value>]".format(
                        name=name
                    )
                elif optiond.bool_value:
                    option_show = "--[!]{name}".format(name=name)
                else:
                    option_show = "--{name}=<value>/{name}=<value>".format(name=name)
                if not option_description:
                    if optiond.plugin_name:
                        option_description = "added by {}".format(optiond.plugin_name)
                    else:
                        option_description = "NO DESCRIPTION"
                print(option_show, option_description)

    def main(self):
        if self.options["show_helps"]:
            self.show_helps()
            return
        if len(self.options["actions"]) > 0:
            for aname in self.options["actions"]:
                if "(" in aname and aname.endswith(")"):
                    parts = aname.split("(")
                    true_or_panic(
                        len(parts) == 2,
                        "found too more ( in your action call {}, could not parse it correctly".format(
                            aname
                        ),
                    )
                    name = parts[0]
                    arg = parts[1][:-1]
                    self.action(name, arg)
                else:
                    self.action(aname)
        if self.options["do_compile"] or self._autorun_compile:
            self.compile()

    def build_sandbox(self):
        sandbox = Sandbox(self.globalconfig["root_config_path"], **self.globalconfig)
        sandbox.ready()
        return sandbox

    def compile(self):
        self.build_sandbox().compile()

    def list_actions(self):
        sandbox = self.build_sandbox()
        action_conf: Dict[str, str] = sandbox.get_actions_conf()
        print('All actions declared in "{}":'.format(sandbox.confpath))
        for k in action_conf.keys():
            if sandbox.is_action_exists(k):
                print("  {} -> {}".format(k, action_conf[k]))
            else:
                print("  {} -> {} (not found)".format(k, action_conf[k]))
        if self.options["vars"].get("all", None):
            print("Private actions:")
            for k in sandbox.private_actions.keys():
                print("  {} -> {}".format(k, sandbox.private_actions[k]))

    def action(self, name, arg=None):
        """
        Call (public or private) action called `name` by `arg`.
        Return the return value of the call.
        """
        sandbox = self.build_sandbox()
        if arg:
            sandbox.config["action_arg"] = arg
        result = sandbox.run_action(name, arg)
        if self.globalconfig["vars"].get("action-print-return", False):
            print(result)
        return result

    @property
    def gvars(self) -> Dict[str, Any]:
        return self.globalconfig["vars"]

    def set_var(self, vars, key, value):
        option_d = self.option_descriptions.get(key, None)
        if option_d:
            if option_d.mix_into:
                self.set_var(vars, option_d.mix_into, value)
            elif option_d.multiple:
                if key not in vars:
                    vars[key] = []
                elif not isinstance(vars[key], list):
                    v = vars[key]
                    vars[key] = [v]
                vars[key].append(value)
            elif option_d.bool_value:
                if not isinstance(value, bool):
                    print(
                        "WARN variable {}={} is forced to convert to boolean as plugin {} define".format(
                            key, value, option_d.plugin_name
                        )
                    )
                    value = not not value
                vars[key] = value
            else:
                vars[key] = value
        else:
            vars[key] = value

    def scanflags(self):
        options = {
            "actions": [],
            "do_compile": False,
            "vars": {},
            "show_helps": False,
        }
        shell_like_action_arg = False
        for arg in self.arguments:
            if arg.startswith("--"):
                parts = arg[2:].split("=")
                if len(parts) == 1:
                    key = parts[0]
                    if key[0] == "!":
                        self.set_var(options["vars"], key[1:], False)
                    else:
                        self.set_var(options["vars"], key, True)
                elif len(parts) == 2:
                    key = parts[0]
                    value = self.str2val(parts[1])
                    self.set_var(options["vars"], key, value)
                else:
                    panic(
                        "could not parse command line argument: undefined format {}, use -h option for help".format(
                            arg
                        )
                    )
            elif "=" in arg:
                parts = arg.split("=")
                true_or_panic(
                    len(parts) == 2,
                    "could not parse command line argument: undefined format {}, use -h option for help".format(
                        arg
                    ),
                )
                self.set_var(options["vars"], parts[0], self.str2val(parts[1]))
            elif arg.startswith(":"):
                options["actions"].append(arg[1:])
                self._autorun_compile = False
                shell_like_action_arg = True
            elif arg == "-C":
                options["do_compile"] = True
            elif arg == "-h":
                options["show_helps"] = True
            else:
                if shell_like_action_arg:
                    a = options["actions"][-1]
                    options["actions"][-1] = "{}({})".format(a, arg)
                    shell_like_action_arg = False
                else:
                    panic(
                        "could not parse command line argument: unknown option {}, use -h option for help".format(
                            arg
                        )
                    )
        return options

    @staticmethod
    def correct_config_path(path):
        if os.path.isdir(path):
            return os.path.join(path, "makru.yaml")
        else:
            return path

    @staticmethod
    def str2val(s):
        def isnum(s):
            number_strs = list(map(str, range(0, 10)))
            is_num = False
            if len(s) == 1:
                return s in number_strs
            else:
                return (s[0] in number_strs) and isnum(s)

        if (s.startswith('""') and s.endswith('""')) or (
            s.startswith("''") and s.endswith("''")
        ):
            return s[1:-1]
        if s == "true":
            return True
        elif s == "false":
            return False
        elif isnum(s):
            return int(s)
        else:
            return s
