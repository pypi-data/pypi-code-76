"""
# cdk8s-redis-sts  ![Release](https://github.com/opencdk8s/cdk8s-redis-sts/workflows/Release/badge.svg?branch=development)

Create a Replicated Redis Statefulset on Kubernetes, powered by the [cdk8s project](https://cdk8s.io) 🚀

## Disclaimer

This construct is under heavy development, and breaking changes will be introduced very often. Please don't forget to version lock your code if you are using this construct.

## Overview

**cdk8s-redis-sts** is a [cdk8s](https://cdk8s.io) library.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from constructs import Construct
from cdk8s import App, Chart, ChartProps
from opencdk8s.cdk8s_redis_sts import MyRedis

class MyChart(Chart):
    def __init__(self, scope, id, *, namespace=None, labels=None):
        super().__init__(scope, id, namespace=namespace, labels=labels)
        MyRedis(self, "dev",
            image="redis",
            namespace="databases",
            volume_size="10Gi",
            replicas=2,
            create_storage_class=True,
            volume_provisioner="kubernetes.io/aws-ebs",
            storage_class_name="io1-slow",
            storage_class_params={
                "type": "io1",
                "fs_type": "ext4",
                "iops_per_gB": "10"
            }
        )

app = App()
MyChart(app, "dev")
app.synth()
```

Then the Kubernetes manifests created by `cdk8s synth` command will have Kubernetes resources such as `Statefulset`, `ConfigMap` and `Service` as follows.

<details>
<summary>manifest.k8s.yaml</summary>

```yaml
allowVolumeExpansion: true
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: io1-slow
parameters:
  fsType: ext4
  iopsPerGB: "10"
  type: io1
provisioner: kubernetes.io/aws-ebs
reclaimPolicy: Retain
---
apiVersion: v1
data:
  master.conf: |-

    bind 0.0.0.0
    daemonize no
    port 6379
    tcp-backlog 511
    timeout 0
    tcp-keepalive 300
    supervised no
  slave.conf: |-

    slaveof dev 6379
kind: ConfigMap
metadata:
  name: dev-redis-conf
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: dev
  name: dev
  namespace: databases
spec:
  ports:
    - port: 6379
      targetPort: 6379
  selector:
    app: dev
  type: ClusterIP
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  labels:
    app: dev
  name: dev
  namespace: databases
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dev
  serviceName: dev
  template:
    metadata:
      labels:
        app: dev
    spec:
      containers:
        - command:
            - bash
            - -c
            - |-
              [[ `hostname` =~ -([0-9]+)$ ]] || exit 1
              ordinal=${BASH_REMATCH[1]}
              if [[ $ordinal -eq 0 ]]; then
              redis-server /mnt/redis/master.conf
              else
              redis-server /mnt/redis/slave.conf
              fi
          env: []
          image: redis
          name: redis
          ports:
            - containerPort: 6379
          resources:
            limits:
              cpu: 400m
              memory: 512Mi
            requests:
              cpu: 200m
              memory: 256Mi
          volumeMounts:
            - mountPath: /data
              name: dev
            - mountPath: /mnt/redis/
              name: dev-redis-conf
      terminationGracePeriodSeconds: 10
      volumes:
        - configMap:
            name: dev-redis-conf
          name: dev-redis-conf
  volumeClaimTemplates:
    - metadata:
        name: dev
        namespace: databases
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
        storageClassName: io1-slow
```

</details>

## Installation

### TypeScript

Use `yarn` or `npm` to install.

```sh
$ npm install @opencdk8s/cdk8s-redis-sts
```

```sh
$ yarn add @opencdk8s/cdk8s-redis-sts
```

### Python

```sh
$ pip install cdk8s-redis-sts
```

## Contribution

1. Fork ([link](https://github.com/opencdk8s/cdk8s-redis-sts/fork))
2. Bootstrap the repo:

   ```bash
   npx projen   # generates package.json
   yarn install # installs dependencies
   ```
3. Development scripts:
   |Command|Description
   |-|-
   |`yarn compile`|Compiles typescript => javascript
   |`yarn watch`|Watch & compile
   |`yarn test`|Run unit test & linter through jest
   |`yarn test -u`|Update jest snapshots
   |`yarn run package`|Creates a `dist` with packages for all languages.
   |`yarn build`|Compile + test + package
   |`yarn bump`|Bump version (with changelog) based on [conventional commits]
   |`yarn release`|Bump + push to `master`
4. Create a feature branch
5. Commit your changes
6. Rebase your local changes against the master branch
7. Create a new Pull Request (use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the title please)

## Licence

[Apache License, Version 2.0](./LICENSE)

## Author

[Hunter-Thompson](https://github.com/Hunter-Thompson)
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

import constructs


class MyRedis(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-redis-sts.MyRedis",
):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        image: builtins.str,
        namespace: builtins.str,
        config_map_name: typing.Optional[builtins.str] = None,
        create_storage_class: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_selector_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        replicas: typing.Optional[jsii.Number] = None,
        resources: typing.Optional["ResourceRequirements"] = None,
        storage_class_name: typing.Optional[builtins.str] = None,
        storage_class_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        volume_provisioner: typing.Optional[builtins.str] = None,
        volume_size: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param name: -
        :param image: (experimental) Container image.
        :param namespace: (experimental) namespace. Default: - default
        :param config_map_name: (experimental) The name of the configmap to use instead of the default one.
        :param create_storage_class: (experimental) Option to create storage class, if enabled, a storage class will be created for the statefulset. Default: true
        :param env: (experimental) Environment variables to pass to the pod.
        :param labels: (experimental) Additional labels to apply to resources. Default: - none
        :param node_selector_params: (experimental) nodeSelector params. Default: - undefined
        :param replicas: Default: 1
        :param resources: (experimental) Resources requests for the DB. Default: - Requests = { CPU = 200m, Mem = 256Mi }, Limits = { CPU = 400m, Mem = 512Mi }
        :param storage_class_name: (experimental) The storage class to use for our PVC. Default: 'gp2-expandable'
        :param storage_class_params: (experimental) Storage class params. Default: - { type = gp2, fsType: ext4 }
        :param volume_provisioner: (experimental) Each StorageClass has a provisioner that determines what volume plugin is used for provisioning PVs. This field must be specified. See `this <https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner>`_ for Ref Default: 'kubernetes.io/aws-ebs'
        :param volume_size: (experimental) The Volume size of our DB in string, e.g 10Gi, 20Gi.

        :stability: experimental
        """
        opts = StsOpts(
            image=image,
            namespace=namespace,
            config_map_name=config_map_name,
            create_storage_class=create_storage_class,
            env=env,
            labels=labels,
            node_selector_params=node_selector_params,
            replicas=replicas,
            resources=resources,
            storage_class_name=storage_class_name,
            storage_class_params=storage_class_params,
            volume_provisioner=volume_provisioner,
            volume_size=volume_size,
        )

        jsii.create(MyRedis, self, [scope, name, opts])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """
        :stability: experimental
        """
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        """
        :stability: experimental
        """
        return typing.cast(builtins.str, jsii.get(self, "namespace"))


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-redis-sts.ResourceQuantity",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class ResourceQuantity:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param cpu: Default: - no limit
        :param memory: Default: - no limit

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        """
        :default: - no limit

        :stability: experimental
        """
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        """
        :default: - no limit

        :stability: experimental
        """
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceQuantity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-redis-sts.ResourceRequirements",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class ResourceRequirements:
    def __init__(
        self,
        *,
        limits: typing.Optional[ResourceQuantity] = None,
        requests: typing.Optional[ResourceQuantity] = None,
    ) -> None:
        """
        :param limits: (experimental) Maximum resources for the web app. Default: - CPU = 400m, Mem = 512Mi
        :param requests: (experimental) Required resources for the web app. Default: - CPU = 200m, Mem = 256Mi

        :stability: experimental
        """
        if isinstance(limits, dict):
            limits = ResourceQuantity(**limits)
        if isinstance(requests, dict):
            requests = ResourceQuantity(**requests)
        self._values: typing.Dict[str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits
        if requests is not None:
            self._values["requests"] = requests

    @builtins.property
    def limits(self) -> typing.Optional[ResourceQuantity]:
        """(experimental) Maximum resources for the web app.

        :default: - CPU = 400m, Mem = 512Mi

        :stability: experimental
        """
        result = self._values.get("limits")
        return typing.cast(typing.Optional[ResourceQuantity], result)

    @builtins.property
    def requests(self) -> typing.Optional[ResourceQuantity]:
        """(experimental) Required resources for the web app.

        :default: - CPU = 200m, Mem = 256Mi

        :stability: experimental
        """
        result = self._values.get("requests")
        return typing.cast(typing.Optional[ResourceQuantity], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceRequirements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-redis-sts.StsOpts",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "namespace": "namespace",
        "config_map_name": "configMapName",
        "create_storage_class": "createStorageClass",
        "env": "env",
        "labels": "labels",
        "node_selector_params": "nodeSelectorParams",
        "replicas": "replicas",
        "resources": "resources",
        "storage_class_name": "storageClassName",
        "storage_class_params": "storageClassParams",
        "volume_provisioner": "volumeProvisioner",
        "volume_size": "volumeSize",
    },
)
class StsOpts:
    def __init__(
        self,
        *,
        image: builtins.str,
        namespace: builtins.str,
        config_map_name: typing.Optional[builtins.str] = None,
        create_storage_class: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_selector_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        replicas: typing.Optional[jsii.Number] = None,
        resources: typing.Optional[ResourceRequirements] = None,
        storage_class_name: typing.Optional[builtins.str] = None,
        storage_class_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        volume_provisioner: typing.Optional[builtins.str] = None,
        volume_size: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param image: (experimental) Container image.
        :param namespace: (experimental) namespace. Default: - default
        :param config_map_name: (experimental) The name of the configmap to use instead of the default one.
        :param create_storage_class: (experimental) Option to create storage class, if enabled, a storage class will be created for the statefulset. Default: true
        :param env: (experimental) Environment variables to pass to the pod.
        :param labels: (experimental) Additional labels to apply to resources. Default: - none
        :param node_selector_params: (experimental) nodeSelector params. Default: - undefined
        :param replicas: Default: 1
        :param resources: (experimental) Resources requests for the DB. Default: - Requests = { CPU = 200m, Mem = 256Mi }, Limits = { CPU = 400m, Mem = 512Mi }
        :param storage_class_name: (experimental) The storage class to use for our PVC. Default: 'gp2-expandable'
        :param storage_class_params: (experimental) Storage class params. Default: - { type = gp2, fsType: ext4 }
        :param volume_provisioner: (experimental) Each StorageClass has a provisioner that determines what volume plugin is used for provisioning PVs. This field must be specified. See `this <https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner>`_ for Ref Default: 'kubernetes.io/aws-ebs'
        :param volume_size: (experimental) The Volume size of our DB in string, e.g 10Gi, 20Gi.

        :stability: experimental
        """
        if isinstance(resources, dict):
            resources = ResourceRequirements(**resources)
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
            "namespace": namespace,
        }
        if config_map_name is not None:
            self._values["config_map_name"] = config_map_name
        if create_storage_class is not None:
            self._values["create_storage_class"] = create_storage_class
        if env is not None:
            self._values["env"] = env
        if labels is not None:
            self._values["labels"] = labels
        if node_selector_params is not None:
            self._values["node_selector_params"] = node_selector_params
        if replicas is not None:
            self._values["replicas"] = replicas
        if resources is not None:
            self._values["resources"] = resources
        if storage_class_name is not None:
            self._values["storage_class_name"] = storage_class_name
        if storage_class_params is not None:
            self._values["storage_class_params"] = storage_class_params
        if volume_provisioner is not None:
            self._values["volume_provisioner"] = volume_provisioner
        if volume_size is not None:
            self._values["volume_size"] = volume_size

    @builtins.property
    def image(self) -> builtins.str:
        """(experimental) Container image.

        :stability: experimental
        """
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        """(experimental) namespace.

        :default: - default

        :stability: experimental
        """
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_map_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the configmap to use instead of the default one.

        :stability: experimental
        """
        result = self._values.get("config_map_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_storage_class(self) -> typing.Optional[builtins.bool]:
        """(experimental) Option to create storage class, if enabled, a storage class will be created for the statefulset.

        :default: true

        :stability: experimental
        """
        result = self._values.get("create_storage_class")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Environment variables to pass to the pod.

        :stability: experimental
        """
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Additional labels to apply to resources.

        :default: - none

        :stability: experimental
        """
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_selector_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) nodeSelector params.

        :default: - undefined

        :stability: experimental
        """
        result = self._values.get("node_selector_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        """
        :default: 1

        :stability: experimental
        """
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resources(self) -> typing.Optional[ResourceRequirements]:
        """(experimental) Resources requests for the DB.

        :default: - Requests = { CPU = 200m, Mem = 256Mi }, Limits = { CPU = 400m, Mem = 512Mi }

        :stability: experimental
        """
        result = self._values.get("resources")
        return typing.cast(typing.Optional[ResourceRequirements], result)

    @builtins.property
    def storage_class_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The storage class to use for our PVC.

        :default: 'gp2-expandable'

        :stability: experimental
        """
        result = self._values.get("storage_class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Storage class params.

        :default: - { type = gp2, fsType: ext4 }

        :stability: experimental
        """
        result = self._values.get("storage_class_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def volume_provisioner(self) -> typing.Optional[builtins.str]:
        """(experimental) Each StorageClass has a provisioner that determines what volume plugin is used for provisioning PVs.

        This field must be specified.
        See `this <https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner>`_ for Ref

        :default: 'kubernetes.io/aws-ebs'

        :stability: experimental
        """
        result = self._values.get("volume_provisioner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[builtins.str]:
        """(experimental) The Volume size of our DB in string, e.g 10Gi, 20Gi.

        :stability: experimental
        """
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StsOpts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MyRedis",
    "ResourceQuantity",
    "ResourceRequirements",
    "StsOpts",
]

publication.publish()
