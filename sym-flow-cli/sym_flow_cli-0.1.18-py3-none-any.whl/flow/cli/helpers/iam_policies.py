import json
from typing import Literal, Sequence

from policy_sentry.querying.arns import get_matching_raw_arns
from policy_sentry.writing.sid_group import SidGroup
from sym.cli.errors import CliError

# This class is used to support the `sym_resources` TF resource.
# Users can specify AWS resource ARNs to wrap a Sym workflow around,
# and this class can generate the appropriate read/write/admin policies
# for those resources, automatically.

PolicyAction = Literal["read", "write", "list", "tagging", "permissions-management"]
PolicySizeLimit = 2048


class IAMPolicies:
    def __init__(self, name: str = ""):
        self.name = name
        self.arns = []

    def add_arn(self, arn: str):
        if not arn.startswith("arn:"):
            arn = f"arn:{arn}"
        try:
            valid = bool(get_matching_raw_arns(arn))
        except:
            valid = False
        if not valid:
            raise CliError(f"Invalid ARN: {arn}")
        self.arns.append(arn)

    def policy_for(self, *actions: Sequence[PolicyAction], name: str = ""):
        template = {"mode": "crud", "name": f"{self.name}{name}"}
        for action in actions:
            template[action] = self.arns.copy()
        sid_group = SidGroup()
        policy = sid_group.process_template(template)
        if len(json.dumps(policy).replace(" ", "")) > PolicySizeLimit:
            policy = sid_group.process_template(template, minimize=True)
        return json.dumps(policy, indent=4)

    def read_policy(self):
        return self.policy_for("read", "list", name="ReadOnly")

    def write_policy(self):
        return self.policy_for("read", "list", "write", name="ReadWrite")

    def admin_policy(self):
        return self.policy_for(
            "read", "list", "write", "tagging", "permissions-management", name="Admin"
        )
