'''
# NightyNight!

Do you have a EC2 instance or an RDS instance that you only need during certain hours of the day? Do you want to reduce it's cost? How about just stopping it every night?

That's the NightyNight construct. It's very simple. Give it an `instanceId` and it will create a Lambda and a CloudWatch Event Rule to fire the lambda at a specific time of day. If the instance is running, it's stopped.

There are currently two variations of the construct:

* [NightyNightForEc2](./API.md#matthewbonig-nightynight-nightynightforec2) - stops an EC2 instance at a given time.
* [NightyNightForRds](./API.md#matthewbonig-nightynight-nightynightforrds) - stops an RDS instance at a given time.
* [NightyNightForAsg](./API.md#matthewbonig-nightynight-nightynightforasg) - sets the desired capacity for an ASG at a given time.

# This is a pre-release!

This is a quick first-draft. All the options that will likely need to be added to accommodate a large
number of use-cases are still needed. If you'd like to make requests or help update this construct, please
open an [Issue](https://github.com/mbonig/nightynight/issues) or a [PR](https://github.com/mbonig/cicd-spa-website/pulls).

# What it creates

![arch.png](./arch.png)

* A Rule that will, on a given schedule, fire a lambda.
* A Lambda with permissions to describe ec2 instances. It will read the instance by the given `instanceId` and then stop the instance if it's in a running state.

# Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..ec2 import NightyNightForEc2

class NightyNightStack(Stack):

    def __init__(self, scope, id, props):
        super().__init__(scope, id, props)

        # The code that defines your stack goes here
        NightyNightForEc2(self, "nighty-night", instance_id="i-123123123123")
```

This will stop the instance with id `i-123123123123` at (the default) 4am GMT.

# API Doc

See the [API Docs](./API.md) for more info.

## Contributing

Please open Pull Requests and Issues on the [Github Repo](https://github.com/mbonig/nightynight).

## License

MIT
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

import aws_cdk.aws_autoscaling
import aws_cdk.aws_events
import aws_cdk.core


class NightyNightForAsg(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForAsg",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will set the given ASG's desired capacity.

    Typically used when you've got and ASG that you can scale during set hours.
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: aws_cdk.aws_autoscaling.IAutoScalingGroup,
        desired_capacity: jsii.Number,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param auto_scaling_group: the instanceId of the EC2 instance you'd like stopped.
        :param desired_capacity: Desired capacity.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        props = NightyNightForAsgProps(
            auto_scaling_group=auto_scaling_group,
            desired_capacity=desired_capacity,
            schedule=schedule,
        )

        jsii.create(NightyNightForAsg, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForAsgProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group": "autoScalingGroup",
        "desired_capacity": "desiredCapacity",
        "schedule": "schedule",
    },
)
class NightyNightForAsgProps:
    def __init__(
        self,
        *,
        auto_scaling_group: aws_cdk.aws_autoscaling.IAutoScalingGroup,
        desired_capacity: jsii.Number,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param auto_scaling_group: the instanceId of the EC2 instance you'd like stopped.
        :param desired_capacity: Desired capacity.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = aws_cdk.aws_events.CronOptions(**schedule)
        self._values: typing.Dict[str, typing.Any] = {
            "auto_scaling_group": auto_scaling_group,
            "desired_capacity": desired_capacity,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def auto_scaling_group(self) -> aws_cdk.aws_autoscaling.IAutoScalingGroup:
        '''the instanceId of the EC2 instance you'd like stopped.'''
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return typing.cast(aws_cdk.aws_autoscaling.IAutoScalingGroup, result)

    @builtins.property
    def desired_capacity(self) -> jsii.Number:
        '''Desired capacity.'''
        result = self._values.get("desired_capacity")
        assert result is not None, "Required property 'desired_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForAsgProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNightForEc2(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForEc2",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will stop the given ec2 instance at the specified time.

    Typically used when you've got ec2 instances that you only need during business hours
    and want to reduce the costs of.
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        instance_id: builtins.str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_id: the instanceId of the EC2 instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        props = NightyNightForEc2Props(instance_id=instance_id, schedule=schedule)

        jsii.create(NightyNightForEc2, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForEc2Props",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId", "schedule": "schedule"},
)
class NightyNightForEc2Props:
    def __init__(
        self,
        *,
        instance_id: builtins.str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param instance_id: the instanceId of the EC2 instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = aws_cdk.aws_events.CronOptions(**schedule)
        self._values: typing.Dict[str, typing.Any] = {
            "instance_id": instance_id,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''the instanceId of the EC2 instance you'd like stopped.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForEc2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNightForRds(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForRds",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will stop the given rds instance at the specified time.

    Typically used when you've got rds instances that you only need during business hours
    and want to reduce the costs of.
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        db_instance_identifier: builtins.str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db_instance_identifier: the DBInstanceIdentifier of the RDS instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        props = NightyNightForRdsProps(
            db_instance_identifier=db_instance_identifier, schedule=schedule
        )

        jsii.create(NightyNightForRds, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForRdsProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_instance_identifier": "dbInstanceIdentifier",
        "schedule": "schedule",
    },
)
class NightyNightForRdsProps:
    def __init__(
        self,
        *,
        db_instance_identifier: builtins.str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param db_instance_identifier: the DBInstanceIdentifier of the RDS instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = aws_cdk.aws_events.CronOptions(**schedule)
        self._values: typing.Dict[str, typing.Any] = {
            "db_instance_identifier": db_instance_identifier,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def db_instance_identifier(self) -> builtins.str:
        '''the DBInstanceIdentifier of the RDS instance you'd like stopped.'''
        result = self._values.get("db_instance_identifier")
        assert result is not None, "Required property 'db_instance_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForRdsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightProps",
    jsii_struct_bases=[NightyNightForEc2Props],
    name_mapping={"instance_id": "instanceId", "schedule": "schedule"},
)
class NightyNightProps(NightyNightForEc2Props):
    def __init__(
        self,
        *,
        instance_id: builtins.str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''
        :param instance_id: the instanceId of the EC2 instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = aws_cdk.aws_events.CronOptions(**schedule)
        self._values: typing.Dict[str, typing.Any] = {
            "instance_id": instance_id,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''the instanceId of the EC2 instance you'd like stopped.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNight(
    NightyNightForEc2,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNight",
):
    '''(deprecated) This class is deprecated, please use NightyNightForEc2.

    :deprecated: in favor of NightyNightForEc2

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        instance_id: builtins.str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_id: the instanceId of the EC2 instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }

        :stability: deprecated
        '''
        props = NightyNightProps(instance_id=instance_id, schedule=schedule)

        jsii.create(NightyNight, self, [scope, id, props])


__all__ = [
    "NightyNight",
    "NightyNightForAsg",
    "NightyNightForAsgProps",
    "NightyNightForEc2",
    "NightyNightForEc2Props",
    "NightyNightForRds",
    "NightyNightForRdsProps",
    "NightyNightProps",
]

publication.publish()
