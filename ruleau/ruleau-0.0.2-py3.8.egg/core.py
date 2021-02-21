from enum import Enum
import logging
import uuid
from typing import Iterable, Optional, Dict
from typing import Any as AnyType
from functools import wraps

logger = logging.getLogger(__name__)


class OverrideLevel(Enum):
    NO_OVERRIDE = 1
    ANY_OVERRIDE = 2


class Rule:
    def __init__(
        self, logic_func, depends_on, override_name, override_level, lazy_dependencies
    ):
        self.logic_func = logic_func
        self.depends_on = depends_on
        self.override_name = override_name
        self.override_level = override_level
        self.__name__ = logic_func.__name__
        self.lazy_dependencies = lazy_dependencies
        self.result = None

    def __call__(self, *args, **kwargs) -> bool:
        print(args, kwargs)
        context = kwargs.get('context') or args[0] or {}
        payload = kwargs.get('payload') or args[1] or {}
        if self.depends_on:
            context.update({func.__name__: func(*args, **kwargs) for func in self.depends_on})
            print('Depends results', context)
        self.result = self.logic_func(context, payload)
        return self.result

    def __str__(self):
        return f"<Rule {self.__name__}>"

    def __repr__(self):
        return str(self)


def rule(
    depends_on=None,
    override_name=None,
    override_level=OverrideLevel.ANY_OVERRIDE,
    lazy_dependencies=False,
):
    """
    Creates a rule from a function
    """
    depends_on = depends_on or []
    override_name = override_name or uuid.uuid4().hex

    def rule_decorator(func):
        return Rule(func, depends_on, override_name, override_level, lazy_dependencies)

    return rule_decorator


def _immutable(func_name):
    def __immutable(self, *args, **kwargs):
        raise TypeError(
            f"'ImmutableDict' object does not support the '{func_name}' operation"
        )

    return __immutable


class ImmutableDict(dict):
    def __init__(self, /, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, val in self.items():
            if isinstance(val, dict):
                self.__setitem__(key, ImmutableDict(val))

            if isinstance(val, list):
                self.__setitem__(key, tuple(val))

    __setitem__ = _immutable("__setitem__")
    __delitem__ = _immutable("__delitem__")
    clear = _immutable("clear")
    update = _immutable("update")  # type: ignore
    setdefault = _immutable("setdefault")
    pop = _immutable("pop")  # type: ignore
    popitem = _immutable("popitem")


def Any(*args):
    @rule(depends_on=args)
    def any_aggregator(context: ExecutionResult, _):
        results = [result.value for result in context.dependant_results]
        return any(results)

    return any_aggregator


def All(*args):
    @rule(depends_on=args)
    def all_aggregator(context: ExecutionResult, _):
        return all(result.value for result in context.dependant_results)

    return all_aggregator


class DependantResults:
    def __init__(self, dependants: Iterable[Rule], payload, overrides, lazy=False):
        self.dependants = {dep.__name__: dep for dep in dependants}
        self.payload = payload
        self.overrides = overrides
        if not lazy:
            self.results_dict = {
                depend.__name__: execute(depend, payload, overrides)
                for depend in dependants
            }
        else:
            self.results_dict = {}

    def __getattr__(self, name):
        try:
            # Enable access to normal python properties
            return super().__getattr__(name)
        except AttributeError:
            # We are trying to find a dependant result
            # TODO: We can tell if the rule will hit this case when the rule is
            # declared, by parsing the AST, which would be friendlier
            if name not in self.dependants:
                depends_on = f"[{', '.join(x for x in self.dependants.keys())}]"
                raise AttributeError(
                    f"Result for rule '{name}' not available, as it was not "
                    f"declared as a dependency. depends_on={depends_on}"
                )

            if name not in self.results_dict:
                self.results_dict[name] = execute(
                    self.dependants[name], self.payload, self.overrides
                )
            return self.results_dict[name]

    def __iter__(self):
        for dep in self.dependants:
            yield self.__getattr__(dep)


class ExecutionResult:
    def __init__(
        self,
        value,
        dependant_results: DependantResults,
        was_overridden: bool = False,
        original_value=None,
    ):
        self.value = value
        self.was_overridden = was_overridden
        self.original_value = original_value
        self.dependant_results = dependant_results


def execute(
    rule: Rule, payload, overrides: Optional[Dict[str, AnyType]] = None
) -> ExecutionResult:
    """
    Executes the provided rule, following dependencies and
    passing in results accordingly
    """
    depend_results = DependantResults(
        rule.depends_on, payload, overrides, lazy=rule.lazy_dependencies
    )
    immutable_payload = ImmutableDict(payload)
    context = ExecutionResult(None, depend_results)

    result = ExecutionResult(rule(context, immutable_payload), depend_results)

    if overrides and rule.override_name in overrides:
        # TODO: We should check on the first call to execute that
        # the overrides specified will actually be used, i.e. it
        # is an error to pass in an override for a rule which doesn't
        # exist

        if rule.override_level == OverrideLevel.NO_OVERRIDE:
            raise Exception(
                "Tried to override rule '{rule.override_name}' "
                "(function '{rule.__name__}'), but override level is "
                "set to NO_OVERRIDE"
            )

        override_result = overrides[rule.override_name]

        logger.info(
            "Overriding result for rule '%s' (function '%s'): new value = '%s'",
            rule.override_name,
            rule.__name__,
            override_result,
        )

        result.was_overridden = True
        result.original_value = result.value
        result.value = override_result

    return result
