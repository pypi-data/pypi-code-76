"""
# cdk-valheim

A high level CDK construct of [Valheim](https://www.valheimgame.com/) dedicated server.

## API

See [API.md](API.md)

## Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ValheimWorld(stack, "ValheimWorld",
    cpu=2048,
    memory_limit_mi_b=4096,
    environment={
        "SERVER_NAME": "CDK Valheim",
        "WORLD_NAME": "Amazon",
        "SERVER_PASS": "fargate"
    }
)
```

## Testing

* Snapshot

```sh
yarn test
```

* Integration

```sh
npx cdk -a "npx ts-node src/integ.valheim.ts" diff
npx cdk -a "npx ts-node src/integ.valheim.ts" deploy
```
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

import aws_cdk.aws_backup
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_efs
import aws_cdk.core


class ValheimWorld(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-valheim.ValheimWorld",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        backup_plan: typing.Optional[aws_cdk.aws_backup.BackupPlan] = None,
        cpu: typing.Optional[jsii.Number] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_system: typing.Optional[aws_cdk.aws_efs.FileSystem] = None,
        image: typing.Optional[aws_cdk.aws_ecs.ContainerImage] = None,
        log_group: typing.Optional[aws_cdk.aws_ecs.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param backup_plan: AWS Backup plan for EFS. Default: - Hourly backup with 3 days retension.
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param desired_count: Desired count of Fargate container. Set 0 for maintenance. Default: - 1
        :param environment: https://github.com/lloesche/valheim-server-docker#environment-variables.
        :param file_system: Persistent storage for save data. Default: - Amazon EFS for default persistent storage.
        :param image: 
        :param log_group: Valheim Server log Group. Default: - Create the new AWS Cloudwatch Log Group for Valheim Server.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs
        """
        props = ValheimWorldProps(
            backup_plan=backup_plan,
            cpu=cpu,
            desired_count=desired_count,
            environment=environment,
            file_system=file_system,
            image=image,
            log_group=log_group,
            memory_limit_mib=memory_limit_mib,
            vpc=vpc,
        )

        jsii.create(ValheimWorld, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> aws_cdk.aws_backup.BackupPlan:
        return typing.cast(aws_cdk.aws_backup.BackupPlan, jsii.get(self, "backupPlan"))

    @backup_plan.setter
    def backup_plan(self, value: aws_cdk.aws_backup.BackupPlan) -> None:
        jsii.set(self, "backupPlan", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> aws_cdk.aws_efs.FileSystem:
        return typing.cast(aws_cdk.aws_efs.FileSystem, jsii.get(self, "fileSystem"))

    @file_system.setter
    def file_system(self, value: aws_cdk.aws_efs.FileSystem) -> None:
        jsii.set(self, "fileSystem", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        return typing.cast(aws_cdk.aws_ecs.FargateService, jsii.get(self, "service"))

    @service.setter
    def service(self, value: aws_cdk.aws_ecs.FargateService) -> None:
        jsii.set(self, "service", value)


@jsii.data_type(
    jsii_type="cdk-valheim.ValheimWorldProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_plan": "backupPlan",
        "cpu": "cpu",
        "desired_count": "desiredCount",
        "environment": "environment",
        "file_system": "fileSystem",
        "image": "image",
        "log_group": "logGroup",
        "memory_limit_mib": "memoryLimitMiB",
        "vpc": "vpc",
    },
)
class ValheimWorldProps:
    def __init__(
        self,
        *,
        backup_plan: typing.Optional[aws_cdk.aws_backup.BackupPlan] = None,
        cpu: typing.Optional[jsii.Number] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_system: typing.Optional[aws_cdk.aws_efs.FileSystem] = None,
        image: typing.Optional[aws_cdk.aws_ecs.ContainerImage] = None,
        log_group: typing.Optional[aws_cdk.aws_ecs.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param backup_plan: AWS Backup plan for EFS. Default: - Hourly backup with 3 days retension.
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param desired_count: Desired count of Fargate container. Set 0 for maintenance. Default: - 1
        :param environment: https://github.com/lloesche/valheim-server-docker#environment-variables.
        :param file_system: Persistent storage for save data. Default: - Amazon EFS for default persistent storage.
        :param image: 
        :param log_group: Valheim Server log Group. Default: - Create the new AWS Cloudwatch Log Group for Valheim Server.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_plan is not None:
            self._values["backup_plan"] = backup_plan
        if cpu is not None:
            self._values["cpu"] = cpu
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if environment is not None:
            self._values["environment"] = environment
        if file_system is not None:
            self._values["file_system"] = file_system
        if image is not None:
            self._values["image"] = image
        if log_group is not None:
            self._values["log_group"] = log_group
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def backup_plan(self) -> typing.Optional[aws_cdk.aws_backup.BackupPlan]:
        """AWS Backup plan for EFS.

        :default: - Hourly backup with 3 days retension.
        """
        result = self._values.get("backup_plan")
        return typing.cast(typing.Optional[aws_cdk.aws_backup.BackupPlan], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)

        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)

        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)

        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)

        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        :default: 1024
        """
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """Desired count of Fargate container.

        Set 0 for maintenance.

        :default: - 1
        """
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """https://github.com/lloesche/valheim-server-docker#environment-variables."""
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file_system(self) -> typing.Optional[aws_cdk.aws_efs.FileSystem]:
        """Persistent storage for save data.

        :default: - Amazon EFS for default persistent storage.
        """
        result = self._values.get("file_system")
        return typing.cast(typing.Optional[aws_cdk.aws_efs.FileSystem], result)

    @builtins.property
    def image(self) -> typing.Optional[aws_cdk.aws_ecs.ContainerImage]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.ContainerImage], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """Valheim Server log Group.

        :default: - Create the new AWS Cloudwatch Log Group for Valheim Server.
        """
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.LogDriver], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        :default: 2048
        """
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where your ECS instances will be running or your ENIs will be deployed.

        :default: - creates a new VPC with two AZs
        """
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValheimWorldProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ValheimWorld",
    "ValheimWorldProps",
]

publication.publish()
