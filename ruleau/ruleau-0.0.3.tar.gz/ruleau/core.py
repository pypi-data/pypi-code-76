from enum import Enum
import logging
import uuid
from typing import Iterable, Optional, Dict
from typing import Any as AnyType
from collections import OrderedDict

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

    def __call__(self, *args, **kwargs):
        return self.logic_func(*args, **kwargs)


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
                depend.__name__: execute(depend, self.payload, self.overrides)
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
        was_overriden: bool = False,
        original_value=None,
    ):
        self.value = value
        self.was_overriden = was_overriden
        self.original_value = original_value
        self.dependant_results = dependant_results


def execute(
    rule: Rule, payload, overrides: Optional[Dict[str, AnyType]] = None
) -> ExecutionResult:
    """
    Executes the provided rule, following dependencies and
    passing in results accordingly
    """
    immutable_payload = OrderedDict(payload).copy()

    depend_results = DependantResults(
        rule.depends_on, immutable_payload, overrides, lazy=rule.lazy_dependencies
    )
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

        result.was_overriden = True
        result.original_value = result.value
        result.value = override_result

    return result
