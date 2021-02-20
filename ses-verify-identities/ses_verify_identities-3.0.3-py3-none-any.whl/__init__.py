"""
# @seeebiii/ses-verify-identities

This package provides two constructs helping you to verify identities in [AWS SES](https://aws.amazon.com/ses/) using the [AWS CDK](https://aws.amazon.com/cdk/).

For more information about verifying identities in AWS SES, [read the documentation](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.html).

## Install

At the moment only TypeScript/JavaScript is supported.

### npm

```
npm i --save-dev @seeebiii/ses-verify-identities
```

## Usage

### Verify a Domain

```
new VerifySesDomain(this, 'SesDomainVerification', {
  domainName: 'example.org'
});
```

#### Options

* `domainName` A domain name to be used for the SES domain identity, e.g. 'example.org'
* `addTxtRecord` Whether to automatically add a TXT record to the hosed zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: `true`.
* `addMxRecord` Whether to automatically add a MX record to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: `true`.
* `addDkimRecord` Whether to automatically add DKIM records to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: `true`.
* `notificationTopic` An SNS topic where bounces, complaints or delivery notifications can be sent to. If none is provided, a new topic will be created and used for all different notification types.
* `notificationTypes` Select for which notification types you want to configure a topic. Default: `[Bounce, Complaint]`.

### Verify an Email Address

```
new VerifySesEmailAddress(this, 'SesEmailVerification', {
  emailAddress: 'hello@example.org'
});
```

#### Options

* `emailAddress` The email address to be verified, e.g. `hello@example.org`.

## Contributing

I'm happy to receive any contributions!
Just open an issue or pull request :)

These commands should help you while developing:

* `npm run build`      compile typescript to js
* `npm run watch`      watch for changes and compile
* `npm run test`       perform the jest unit tests
* `npm run lint`       validate code against best practices
* `npm run prettier`   format code as configured in config

## Author

[Sebastian Hesse](https://www.sebastianhesse.de) - Freelancer for serverless cloud projects on AWS.

## License

MIT License

Copyright (c) 2020 [Sebastian Hesse](https://www.sebastianhesse.de)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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

import aws_cdk.aws_route53
import aws_cdk.aws_sns
import aws_cdk.core


@jsii.interface(jsii_type="@seeebiii/ses-verify-identities.IVerifySesDomainProps")
class IVerifySesDomainProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IVerifySesDomainPropsProxy"]:
        return _IVerifySesDomainPropsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """A domain name to be used for the SES domain identity, e.g. 'example.org'."""
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addDkimRecords")
    def add_dkim_records(self) -> typing.Optional[builtins.bool]:
        """Whether to automatically add DKIM records to the hosted zone of your domain.

        This only works if your domain is managed by Route53. Otherwise disable it. Default: true.
        """
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addMxRecord")
    def add_mx_record(self) -> typing.Optional[builtins.bool]:
        """Whether to automatically add a MX record to the hosted zone of your domain.

        This only works if your domain is managed by Route53. Otherwise disable it. Default: true.
        """
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addTxtRecord")
    def add_txt_record(self) -> typing.Optional[builtins.bool]:
        """Whether to automatically add a TXT record to the hosed zone of your domain.

        This only works if your domain is managed by Route53. Otherwise disable it. Default: true.
        """
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        """An SNS topic where bounces, complaints or delivery notifications can be sent to.

        If none is provided, a new topic will be created and used for all different notification types.
        """
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTypes")
    def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
        """Select for which notification types you want to configure a topic.

        Default: [Bounce, Complaint].
        """
        ...


class _IVerifySesDomainPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@seeebiii/ses-verify-identities.IVerifySesDomainProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """A domain name to be used for the SES domain identity, e.g. 'example.org'."""
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addDkimRecords")
    def add_dkim_records(self) -> typing.Optional[builtins.bool]:
        """Whether to automatically add DKIM records to the hosted zone of your domain.

        This only works if your domain is managed by Route53. Otherwise disable it. Default: true.
        """
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "addDkimRecords"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addMxRecord")
    def add_mx_record(self) -> typing.Optional[builtins.bool]:
        """Whether to automatically add a MX record to the hosted zone of your domain.

        This only works if your domain is managed by Route53. Otherwise disable it. Default: true.
        """
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "addMxRecord"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addTxtRecord")
    def add_txt_record(self) -> typing.Optional[builtins.bool]:
        """Whether to automatically add a TXT record to the hosed zone of your domain.

        This only works if your domain is managed by Route53. Otherwise disable it. Default: true.
        """
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "addTxtRecord"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        """An SNS topic where bounces, complaints or delivery notifications can be sent to.

        If none is provided, a new topic will be created and used for all different notification types.
        """
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], jsii.get(self, "notificationTopic"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTypes")
    def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
        """Select for which notification types you want to configure a topic.

        Default: [Bounce, Complaint].
        """
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationTypes"))


@jsii.interface(
    jsii_type="@seeebiii/ses-verify-identities.IVerifySesEmailAddressProps"
)
class IVerifySesEmailAddressProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IVerifySesEmailAddressPropsProxy"]:
        return _IVerifySesEmailAddressPropsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        """The email address to be verified, e.g. 'hello@example.org'."""
        ...


class _IVerifySesEmailAddressPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@seeebiii/ses-verify-identities.IVerifySesEmailAddressProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        """The email address to be verified, e.g. 'hello@example.org'."""
        return typing.cast(builtins.str, jsii.get(self, "emailAddress"))


class VerifySesDomain(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-verify-identities.VerifySesDomain",
):
    """A construct to verify a SES domain identity.

    It initiates a domain verification and can automatically create appropriate records in Route53 to verify the domain. Also, it's possible to attach a notification topic for bounces, complaints or delivery notifications.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        VerifySesDomain(self, "SesDomainVerification",
            domain_name="example.org"
        )
    """

    def __init__(
        self,
        parent: aws_cdk.core.Construct,
        name: builtins.str,
        props: IVerifySesDomainProps,
    ) -> None:
        """
        :param parent: -
        :param name: -
        :param props: -
        """
        jsii.create(VerifySesDomain, self, [parent, name, props])

    @jsii.member(jsii_name="getHostedZone")
    def get_hosted_zone(
        self,
        domain_name: builtins.str,
    ) -> aws_cdk.aws_route53.IHostedZone:
        """
        :param domain_name: -
        """
        return typing.cast(aws_cdk.aws_route53.IHostedZone, jsii.invoke(self, "getHostedZone", [domain_name]))


class VerifySesEmailAddress(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-verify-identities.VerifySesEmailAddress",
):
    """A construct to verify an SES email address identity.

    It initiates a verification so that SES sends a verification email to the desired email address. This means the owner of the email address still needs to act by clicking the link in the verification email.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        org""
    """

    def __init__(
        self,
        parent: aws_cdk.core.Construct,
        name: builtins.str,
        props: IVerifySesEmailAddressProps,
    ) -> None:
        """
        :param parent: -
        :param name: -
        :param props: -
        """
        jsii.create(VerifySesEmailAddress, self, [parent, name, props])


__all__ = [
    "IVerifySesDomainProps",
    "IVerifySesEmailAddressProps",
    "VerifySesDomain",
    "VerifySesEmailAddress",
]

publication.publish()
