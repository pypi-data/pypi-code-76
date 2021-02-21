'''
# @seeebiii/ses-email-forwarding

This [AWS CDK](https://aws.amazon.com/cdk/) construct allows you to setup email forwarding mappings in [AWS SES](https://aws.amazon.com/ses/) to receive emails from your domain and forward them to another email address.
All of this is possible without hosting your own email server, you just need a domain.

For example, if you own a domain `example.org` and want to receive emails for `hello@example.org` and `privacy@example.org`, you can forward emails to `whatever@provider.com`.
This is achieved by using a Lambda function that forwards the emails using [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder).

This construct is creating quite a few resources under the hood and can also automatically verify your domain and email addresses in SES.
Consider reading the [Architecture](#architecture) section below if you want to know more about the details.

## Examples

Forward all emails received under `hello@example.org` to `whatever+hello@provider.com`:

```javascript
new EmailForwardingRuleSet(this, 'EmailForwardingRuleSet', {
  // make the underlying rule set the active one
  enableRuleSet: true,
  // define how emails are being forwarded
  emailForwardingProps: [{
    // your domain name you want to use for receiving and sending emails
    domainName: 'example.org',
    // a prefix that is used for the From email address to forward your mails
    fromPrefix: 'noreply',
    // a list of mappings between a prefix and target email address
    emailMappings: [{
      // the prefix matching the receiver address as <prefix>@<domainName>
      receivePrefix: 'hello',
      // the target email address(es) that you want to forward emails to
      targetEmails: ['whatever+hello@provider.com']
    }]
  }]
});
```

Forward all emails to `hello@example.org` to `whatever+hello@provider.com` and verify the domain `example.org` in SES:

```javascript
new EmailForwardingRuleSet(this, 'EmailForwardingRuleSet', {
  emailForwardingProps: [{
    domainName: 'example.org',
    // let the construct automatically verify your domain
    verifyDomain: true,
    fromPrefix: 'noreply',
    emailMappings: [{
      receivePrefix: 'hello',
      targetEmails: ['whatever+hello@provider.com']
    }]
  }]
});
```

If you don't want to verify your domain in SES or you are in the SES sandbox, you can still send emails to verified email addresses.
Use the property `verifyTargetEmailAddresses` in this case and set it to `true`.

For a full & up-to-date reference of the available options, please look at the source code of  [`EmailForwardingRuleSet`](lib/email-forwarding-rule-set.ts) and [`EmailForwardingRule`](lib/email-forwarding-rule.ts).

#### Note

Since the verification of domains requires to lookup the Route53 domains in your account, you need to define your AWS account and region.
You can do it like this in your CDK stack:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

class EmailForwardingSetupStack(cdk.Stack):
    def __init__(self, scope, id, props=None):
        super().__init__(scope, id, props)

        EmailForwardingRuleSet(self, "EmailForwardingRuleSet")

EmailForwardingSetupStack(app, "EmailForwardingSetupStack",
    env={
        "account": "<account-id>",
        "region": "<region>"
    }
)
```

## Use Cases

* Build a landing page on AWS and offer an email address to contact you.
* Use various aliases to register for different services and forward all mails to the same target email address.

There are probably more - happy to hear them :)

## Install

### npm

```shell
npm i -D @seeebiii/ses-email-forwarding
```

Take a look at [package.json](./package.json) to make sure you're installing the correct version compatible with your current AWS CDK version.
See more details on npmjs.com: https://www.npmjs.com/package/@seeebiii/ses-email-forwarding

### Maven

```xml
<dependency>
  <groupId>de.sebastianhesse.cdk-constructs</groupId>
  <artifactId>ses-email-forwarding</artifactId>
  <version>2.0.1</version>
</dependency>
```

See more details on mvnrepository.com: https://mvnrepository.com/artifact/de.sebastianhesse.cdk-constructs/ses-email-forwarding/

### Python

```shell
pip install ses-email-forwarding
```

See more details on PyPi: https://pypi.org/project/ses-email-forwarding/

### Dotnet / C#

You can find the details here: https://www.nuget.org/packages/Ses.Email.Forwarding/

## Usage

This package provides two constructs: [`EmailForwardingRuleSet`](lib/email-forwarding-rule-set.ts) and [`EmailForwardingRule`](lib/email-forwarding-rule.ts).
The `EmailForwardingRuleSet` is a wrapper around `ReceiptRuleSet` but adds a bit more magic to e.g. verify a domain or target email address.
Similarly, `EmailForwardingRule` is a wrapper around `ReceiptRule` but adds two SES rule actions to forward the email addresses appropriately.

This means if you want the full flexibility, you can use the `EmailForwardingRule` construct in your stack.

### Sending E-Mails over SMTP

You can also send emails over SES using this construct because it provides the basics for sending emails: a verified SES domain or email address identity.
You need to do the following if you're using the `EmailForwardingRuleSetConstruct`:

1. Set the `verifyDomain` or `verifyTargetEmailAddresses` to `true`.
2. [Create SMTP credentials in AWS SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html?icmpid=docs_ses_console) and save them somewhere.
3. Setup your email program or application to use the SMTP settings.

## Architecture

The `EmailForwardingRuleSet` creates a `EmailForwardingRule` for each forward mapping.
Each rule contains an `S3Action` to store the incoming emails and a Lambda Function to forward the emails to the target email addresses.
The Lambda function is just a thin wrapper around the [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder) library.
Since this library expects a JSON config with the email mappings, the `EmailForwardingRule` will create an SSM parameter to store the config.
(Note: this is not ideal because an SSM parameter is limited in the size and hence, this might be changed later)
The Lambda function receives a reference to this parameter as an environment variable (and a bit more) and forwards everything to the library.

In order to verify a domain or email address, the `EmailForwardingRuleSet` construct is using the package [@seeebiii/ses-verify-identities](https://www.npmjs.com/package/@seeebiii/ses-verify-identities).
It provides constructs to verify the SES identities.
For domains, it creates appropriate Route53 records like MX, TXT and Cname (for DKIM).
For email addresses, it calls the AWS API to initiate email address verification.

## TODO

* Encrypt email files on S3 bucket by either using S3 bucket encryption (server side) or enable client encryption using SES actions
* Write tests
* Document options/JSDoc in Readme or separate HTML

## Contributing

I'm happy to receive any contributions!
Just open an issue or pull request :)

These commands should help you while developing:

* `npx projen`             synthesize changes in [.projenrc.js](.projenrc.js) to the project
* `npm run build`          compile typescript to js
* `npm run watch`          watch for changes and compile
* `npm run test`           perform the jest unit tests
* `npm run lint`           validate code against best practices

## Thanks

Thanks a lot to [arithmetric](https://github.com/arithmetric) for providing the NPM package [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder).
This CDK construct is using it in the Lambda function to forward the emails.

## Author

[Sebastian Hesse](https://www.sebastianhesse.de) - Freelancer for serverless cloud projects on AWS.

## License

MIT License

Copyright (c) 2020 [Sebastian Hesse](https://www.sebastianhesse.de)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_s3
import aws_cdk.aws_ses
import aws_cdk.aws_sns
import aws_cdk.core


class EmailForwardingRule(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingRule",
):
    '''A construct to define an email forwarding rule that can either be used together with {@link EmailForwardingRuleSet} or as a standalone rule.

    It creates two rule actions:

    - One S3 action to save all incoming mails to an S3 bucket.
    - One Lambda action to forward all incoming mails to a list of configured emails.

    The Lambda function is using the NPM package ``aws-lambda-ses-forwarder`` to forward the mails.
    '''

    def __init__(
        self,
        parent: aws_cdk.core.Construct,
        name: builtins.str,
        props: "IEmailForwardingRuleProps",
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param props: -
        '''
        jsii.create(EmailForwardingRule, self, [parent, name, props])


class EmailForwardingRuleSet(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingRuleSet",
):
    '''A construct for AWS SES to forward all emails of certain domains and email addresses to a list of target email addresses.

    It also verifies (or at least initiates verification of) the related domains and email addresses in SES.

    The construct can be helpful if you don't want to host your own SMTP server but still want to receive emails to your existing email inbox.
    One use case is if you're just building some sort of landing page and want to quickly setup email receiving for your domain without yet another separate email inbox.

    This construct can...

    - create a new receipt rule set (or use an existing one),
    - attach a list of rules to forward incoming emails to other target email addresses,
    - verify a given domain in SES (automatically if domain is managed by Route53, otherwise it'll just initiate the verification),
    - initiate verification for all target email addresses that are provided for receiving the forwarded emails.
    '''

    def __init__(
        self,
        parent: aws_cdk.core.Construct,
        name: builtins.str,
        props: "IEmailForwardingRuleSetProps",
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param props: -
        '''
        jsii.create(EmailForwardingRuleSet, self, [parent, name, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> aws_cdk.aws_ses.ReceiptRuleSet:
        return typing.cast(aws_cdk.aws_ses.ReceiptRuleSet, jsii.get(self, "ruleSet"))

    @rule_set.setter
    def rule_set(self, value: aws_cdk.aws_ses.ReceiptRuleSet) -> None:
        jsii.set(self, "ruleSet", value)


@jsii.interface(jsii_type="@seeebiii/ses-email-forwarding.IEmailForwardingProps")
class IEmailForwardingProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEmailForwardingPropsProxy"]:
        return _IEmailForwardingPropsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name for which you want to receive emails using SES, e.g. ``example.org``.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailMappings")
    def email_mappings(self) -> typing.List["IEmailMapping"]:
        '''A list of email mappings to define the receive email address and target email addresses to which the emails are forwarded to.

        :see: IEmailMapping
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fromPrefix")
    def from_prefix(self) -> builtins.str:
        '''A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''Optional: an S3 bucket to store the received emails.

        If none is provided, a new one will be created.

        :default: A new bucket.
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional: a prefix for the email files that are stored on the S3 bucket.

        :default: inbox/
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        '''Optional: an SNS topic to receive notifications about sending events like bounces or complaints.

        The events are defined by ``notificationTypes`` using {@link NotificationType}. If no topic is defined, a new one will be created.

        :default: A new SNS topic.
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTypes")
    def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: a list of {@link NotificationType}s to define which sending events should be subscribed.

        :default: ['Bounce', 'Complaint']
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="verifyDomain")
    def verify_domain(self) -> typing.Optional[builtins.bool]:
        '''Optional: true if you want to verify the domain identity in SES, false otherwise.

        :default: false
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="verifyTargetEmailAddresses")
    def verify_target_email_addresses(self) -> typing.Optional[builtins.bool]:
        '''Optional: true if you want to initiate the verification of your target email addresses, false otherwise.

        If ``true``, a verification email is sent out to all target email addresses. Then, the owner of an email address needs to verify it by clicking the link in the verification email.
        Please note in case you don't verify your sender domain, it's required to verify your target email addresses in order to send mails to them.

        :default: false
        '''
        ...


class _IEmailForwardingPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@seeebiii/ses-email-forwarding.IEmailForwardingProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name for which you want to receive emails using SES, e.g. ``example.org``.'''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailMappings")
    def email_mappings(self) -> typing.List["IEmailMapping"]:
        '''A list of email mappings to define the receive email address and target email addresses to which the emails are forwarded to.

        :see: IEmailMapping
        '''
        return typing.cast(typing.List["IEmailMapping"], jsii.get(self, "emailMappings"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fromPrefix")
    def from_prefix(self) -> builtins.str:
        '''A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.'''
        return typing.cast(builtins.str, jsii.get(self, "fromPrefix"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''Optional: an S3 bucket to store the received emails.

        If none is provided, a new one will be created.

        :default: A new bucket.
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "bucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional: a prefix for the email files that are stored on the S3 bucket.

        :default: inbox/
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefix"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        '''Optional: an SNS topic to receive notifications about sending events like bounces or complaints.

        The events are defined by ``notificationTypes`` using {@link NotificationType}. If no topic is defined, a new one will be created.

        :default: A new SNS topic.
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], jsii.get(self, "notificationTopic"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTypes")
    def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: a list of {@link NotificationType}s to define which sending events should be subscribed.

        :default: ['Bounce', 'Complaint']
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationTypes"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="verifyDomain")
    def verify_domain(self) -> typing.Optional[builtins.bool]:
        '''Optional: true if you want to verify the domain identity in SES, false otherwise.

        :default: false
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "verifyDomain"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="verifyTargetEmailAddresses")
    def verify_target_email_addresses(self) -> typing.Optional[builtins.bool]:
        '''Optional: true if you want to initiate the verification of your target email addresses, false otherwise.

        If ``true``, a verification email is sent out to all target email addresses. Then, the owner of an email address needs to verify it by clicking the link in the verification email.
        Please note in case you don't verify your sender domain, it's required to verify your target email addresses in order to send mails to them.

        :default: false
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "verifyTargetEmailAddresses"))


@jsii.interface(jsii_type="@seeebiii/ses-email-forwarding.IEmailForwardingRuleProps")
class IEmailForwardingRuleProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEmailForwardingRulePropsProxy"]:
        return _IEmailForwardingRulePropsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name of the email addresses, e.g. 'example.org'. It is used to connect the ``fromPrefix`` and ``receivePrefix`` properties with a proper domain.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailMapping")
    def email_mapping(self) -> typing.List["IEmailMapping"]:
        '''An email mapping similar to what the NPM library ``aws-lambda-ses-forwarder`` expects.

        :see: IEmailMapping
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fromPrefix")
    def from_prefix(self) -> builtins.str:
        '''A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''An id for the rule.

        This will mainly be used to provide a name to the underlying rule but may also be used as a prefix for other resources.
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> aws_cdk.aws_ses.ReceiptRuleSet:
        '''The rule set this rule belongs to.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''A bucket to store the email files to.

        If no bucket is provided, a new one will be created using a managed KMS key to encrypt the bucket.

        :default: A new bucket will be created.
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix for the email files that are saved to the bucket.

        :default: inbox/
        '''
        ...


class _IEmailForwardingRulePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@seeebiii/ses-email-forwarding.IEmailForwardingRuleProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name of the email addresses, e.g. 'example.org'. It is used to connect the ``fromPrefix`` and ``receivePrefix`` properties with a proper domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailMapping")
    def email_mapping(self) -> typing.List["IEmailMapping"]:
        '''An email mapping similar to what the NPM library ``aws-lambda-ses-forwarder`` expects.

        :see: IEmailMapping
        '''
        return typing.cast(typing.List["IEmailMapping"], jsii.get(self, "emailMapping"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fromPrefix")
    def from_prefix(self) -> builtins.str:
        '''A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.'''
        return typing.cast(builtins.str, jsii.get(self, "fromPrefix"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''An id for the rule.

        This will mainly be used to provide a name to the underlying rule but may also be used as a prefix for other resources.
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> aws_cdk.aws_ses.ReceiptRuleSet:
        '''The rule set this rule belongs to.'''
        return typing.cast(aws_cdk.aws_ses.ReceiptRuleSet, jsii.get(self, "ruleSet"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''A bucket to store the email files to.

        If no bucket is provided, a new one will be created using a managed KMS key to encrypt the bucket.

        :default: A new bucket will be created.
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "bucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix for the email files that are saved to the bucket.

        :default: inbox/
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefix"))


@jsii.interface(
    jsii_type="@seeebiii/ses-email-forwarding.IEmailForwardingRuleSetProps"
)
class IEmailForwardingRuleSetProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEmailForwardingRuleSetPropsProxy"]:
        return _IEmailForwardingRuleSetPropsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailForwardingProps")
    def email_forwarding_props(self) -> typing.List[IEmailForwardingProps]:
        '''A list of mapping options to define how emails should be forwarded.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableRuleSet")
    def enable_rule_set(self) -> typing.Optional[builtins.bool]:
        '''Optional: whether to enable the rule set or not.

        :default: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> typing.Optional[aws_cdk.aws_ses.ReceiptRuleSet]:
        '''Optional: an existing SES receipt rule set.

        If none is provided, a new one will be created using the name provided with ``ruleSetName`` or a default one.
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSetName")
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''Optional: provide a name for the receipt rule set that this construct creates if you don't provide one.

        :default: custom-rule-set
        '''
        ...


class _IEmailForwardingRuleSetPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@seeebiii/ses-email-forwarding.IEmailForwardingRuleSetProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailForwardingProps")
    def email_forwarding_props(self) -> typing.List[IEmailForwardingProps]:
        '''A list of mapping options to define how emails should be forwarded.'''
        return typing.cast(typing.List[IEmailForwardingProps], jsii.get(self, "emailForwardingProps"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableRuleSet")
    def enable_rule_set(self) -> typing.Optional[builtins.bool]:
        '''Optional: whether to enable the rule set or not.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableRuleSet"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> typing.Optional[aws_cdk.aws_ses.ReceiptRuleSet]:
        '''Optional: an existing SES receipt rule set.

        If none is provided, a new one will be created using the name provided with ``ruleSetName`` or a default one.
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ses.ReceiptRuleSet], jsii.get(self, "ruleSet"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSetName")
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''Optional: provide a name for the receipt rule set that this construct creates if you don't provide one.

        :default: custom-rule-set
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleSetName"))


@jsii.interface(jsii_type="@seeebiii/ses-email-forwarding.IEmailMapping")
class IEmailMapping(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEmailMappingProxy"]:
        return _IEmailMappingProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetEmails")
    def target_emails(self) -> typing.List[builtins.str]:
        '''A list of target email addresses that should receive the forwarded emails for the given email addresses matched by either ``receiveEmail`` or ``receivePrefix``.

        Make sure that you only specify email addresses that are verified by SES. Otherwise SES won't send them out.

        Example: ``['foobar@gmail.com', 'foo+bar@gmail.com', 'whatever@example.org']``
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="receiveEmail")
    def receive_email(self) -> typing.Optional[builtins.str]:
        '''You can define a string that is matching an email address, e.g. ``hello@example.org``.

        If this property is defined, the ``receivePrefix`` will be ignored. You must define either this property or ``receivePrefix``, otherwise no emails will be forwarded.
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="receivePrefix")
    def receive_prefix(self) -> typing.Optional[builtins.str]:
        '''A short way to match a specific email addresses by only providing a prefix, e.g. ``hello``. The prefix will be combined with the given domain name from {@link IEmailForwardingRuleProps}. If an email was sent to this specific email address, all emails matching this receiver will be forwarded to all email addresses defined in ``targetEmails``.

        If ``receiveEmail`` property is defined as well, then ``receiveEmail`` is preferred. Hence, only define one of them.
        '''
        ...


class _IEmailMappingProxy:
    __jsii_type__: typing.ClassVar[str] = "@seeebiii/ses-email-forwarding.IEmailMapping"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetEmails")
    def target_emails(self) -> typing.List[builtins.str]:
        '''A list of target email addresses that should receive the forwarded emails for the given email addresses matched by either ``receiveEmail`` or ``receivePrefix``.

        Make sure that you only specify email addresses that are verified by SES. Otherwise SES won't send them out.

        Example: ``['foobar@gmail.com', 'foo+bar@gmail.com', 'whatever@example.org']``
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetEmails"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="receiveEmail")
    def receive_email(self) -> typing.Optional[builtins.str]:
        '''You can define a string that is matching an email address, e.g. ``hello@example.org``.

        If this property is defined, the ``receivePrefix`` will be ignored. You must define either this property or ``receivePrefix``, otherwise no emails will be forwarded.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "receiveEmail"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="receivePrefix")
    def receive_prefix(self) -> typing.Optional[builtins.str]:
        '''A short way to match a specific email addresses by only providing a prefix, e.g. ``hello``. The prefix will be combined with the given domain name from {@link IEmailForwardingRuleProps}. If an email was sent to this specific email address, all emails matching this receiver will be forwarded to all email addresses defined in ``targetEmails``.

        If ``receiveEmail`` property is defined as well, then ``receiveEmail`` is preferred. Hence, only define one of them.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "receivePrefix"))


__all__ = [
    "EmailForwardingRule",
    "EmailForwardingRuleSet",
    "IEmailForwardingProps",
    "IEmailForwardingRuleProps",
    "IEmailForwardingRuleSetProps",
    "IEmailMapping",
]

publication.publish()
