from typing import List
from collections import namedtuple

import yaml
from kubernetes import client, config
from kubernetes.client.models.v1_service_list import V1ServiceList
from kubernetes.client.models.v1_service import V1Service
from kubernetes.client.models.v1_object_meta import V1ObjectMeta

UstatePair = namedtuple("UstatePair", "name libversion")


def _get_ustate_instances(ns) -> V1ServiceList:
    config.load_kube_config()
    v1 = client.CoreV1Api()
    svcs = v1.list_namespaced_service(ns)
    item: V1Service
    meta: V1ObjectMeta
    ustates: List[UstatePair] = []
    for svc in svcs.items:
        meta = svc.metadata
        if meta.name.startswith("ustate-"):
            if svc.metadata.name and svc.metadata.labels:
                u = UstatePair(name=svc.metadata.name, libversion=svc.metadata.labels.get('libversion'))
                ustates.append(u)
    return ustates


def prep_ustate_kube_versions(ns, dest):
    ustates = _get_ustate_instances(ns)
    values = []
    for ustate in ustates:
        values.append({
            "ServiceName": str(ustate.name),
            "LibVersion": str(ustate.libversion)
        })
    versions = {
        "versions": values
    }
    with open(dest, "wt") as fp:
        yaml.dump(versions, fp)
