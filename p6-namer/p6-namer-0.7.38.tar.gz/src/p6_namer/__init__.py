"""
AWS CDK setups up a Custom Resource via Cloud Formation which sets
the AWS IAM Account Alias

# P6Namer

* [P6Namer](#p6namer)

  * [Badges](#badges)
  * [Distributions](#distributions)
  * [Summary](#summary)
  * [Contributing](#contributing)
  * [Code of Conduct](#code-of-conduct)
  * [Changes](#changes)

    * [Usage](#usage)
  * [Author](#author)

## Badges

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/p6m7g8/p6-namer)
![Build](https://github.com/p6m7g8/p6-namer/workflows/Build/badge.svg)
![Release](https://github.com/p6m7g8/p6-namer/workflows/Release/badge.svg)
[![Mergify](https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/p6m7g8/p6-namer/&style=flat)](https://mergify.io)
[![codecov](https://codecov.io/gh/p6m7g8/p6-namer/branch/master/graph/badge.svg?token=14Yj1fZbew)](https://codecov.io/gh/p6m7g8/p6-namer)
[![Known Vulnerabilities](https://snyk.io/test/github/p6m7g8/p6-namer/badge.svg?targetFile=package.json)](https://snyk.io/test/github/p6m7g8/p6-namer?targetFile=package.json)
[![Gihub repo dependents](https://badgen.net/github/dependents-repo/p6m7g8/p6-namer)](https://github.com/p6m7g8/p6-namer/network/dependents?dependent_type=REPOSITORY)
[![Gihub package dependents](https://badgen.net/github/dependents-pkg/p6m7g8/p6-namer)](https://github.com/p6m7g8/p6-namer/network/dependents?dependent_type=PACKAGE)

## Distributions

[![npm version](https://badge.fury.io/js/p6-namer.svg)](https://badge.fury.io/js/p6-namer)
[![PyPI version](https://badge.fury.io/py/p6-namer.svg)](https://badge.fury.io/py/p6-namer)
[![NuGet version](https://badge.fury.io/nu/P6m7g8.P6Namer.svg)](https://badge.fury.io/nu/P6m7g8.P6Namer)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.github.p6m7g8/p6-namer/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.github.p6m7g8/p6-namer)

## Summary

Deploys Custom Resource backed by a Lambda function with `iam:CreateAccountAlias` permissions.
This function is idempotent so can be re-run with the same input.

## Contributing

* [How to Contribute](CONTRIBUTING.md)

## Code of Conduct

* [Code of Conduct](CODE_OF_CONDUCT.md)

## Changes

* [Change Log](CHANGELOG.md)

### Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from p6_namer import P6Namer

P6Namer(self, "AccountAlias",
    account_alias="THE-ALIAS"
)
```

## Author

Philip M. Gollucci [pgollucci@p6m7g8.com](mailto:pgollucci@p6m7g8.com)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.interface(jsii_type="p6-namer.IP6NamerProps")
class IP6NamerProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IP6NamerPropsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accountAlias")
    def account_alias(self) -> builtins.str:
        ...

    @account_alias.setter # type: ignore
    def account_alias(self, value: builtins.str) -> None:
        ...


class _IP6NamerPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "p6-namer.IP6NamerProps"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accountAlias")
    def account_alias(self) -> builtins.str:
        return jsii.get(self, "accountAlias")

    @account_alias.setter # type: ignore
    def account_alias(self, value: builtins.str) -> None:
        jsii.set(self, "accountAlias", value)


class P6Namer(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="p6-namer.P6Namer",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IP6NamerProps,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        """
        jsii.create(P6Namer, self, [scope, id, props])


__all__ = [
    "IP6NamerProps",
    "P6Namer",
]

publication.publish()
